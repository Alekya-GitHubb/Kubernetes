import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# This looks for the Environment Variable 'INVENTORY_SERVICE_URL'
# If not found (like when running locally without Docker), it defaults to localhost:5001
BACKEND_URL = os.environ.get('INVENTORY_SERVICE_URL', 'http://localhost:5001')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StoreManager</title>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #e0f7fa; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #006064; text-align: center; }
        .item { display: flex; justify-content: space-between; border-bottom: 1px solid #eee; padding: 10px 0; }
        button { cursor: pointer; background: #00bcd4; color: white; border: none; padding: 5px 10px; }
        .warning { background: #ffebee; color: #c62828; padding: 10px; display: none; margin-bottom: 10px;}
    </style>
</head>
<body>
    <div class="container">
        <h1>StoreManager</h1>
        
        <div id="error-msg" class="warning">Error: Cannot connect to Backend Service!</div>

        <div style="background: #eee; padding: 15px; margin-bottom: 20px;">
            <input type="text" id="name" placeholder="Name">
            <input type="number" id="quantity" placeholder="Qty">
            <input type="number" id="price" placeholder="Price">
            <button onclick="addItem()">Add Item</button>
        </div>
        <div id="list">Loading...</div>
    </div>

    <script>
        // The browser talks to the Frontend Server (Proxy), not the Backend directly
        const PROXY_URL = "/proxy/items";

        async function loadItems() {
            try {
                const res = await fetch(PROXY_URL);
                if (!res.ok) throw new Error("Backend Error");
                const items = await res.json();
                
                document.getElementById('list').innerHTML = items.map(i => `
                    <div class="item">
                        <span>${i.name} (x${i.quantity}) - $${i.price}</span>
                        <button onclick="deleteItem('${i.id}')">Delete</button>
                    </div>
                `).join('');
                document.getElementById('error-msg').style.display = 'none';
            } catch (e) {
                document.getElementById('error-msg').style.display = 'block';
                document.getElementById('list').innerHTML = "Connection Failed.";
            }
        }

        async function addItem() {
            const name = document.getElementById('name').value;
            const quantity = document.getElementById('quantity').value;
            const price = document.getElementById('price').value;
            await fetch(PROXY_URL, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ name, quantity, price })
            });
            document.getElementById('name').value = ''; 
            loadItems();
        }

        async function deleteItem(id) {
            await fetch(`${PROXY_URL}/${id}`, { method: 'DELETE' });
            loadItems();
        }

        loadItems();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# --- PROXY ROUTES ---
# These routes forward requests from the browser to the Backend Service
@app.route('/proxy/items', methods=['GET'])
def proxy_get():
    try:
        resp = requests.get(f"{BACKEND_URL}/api/items")
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Backend is down"}), 503

@app.route('/proxy/items', methods=['POST'])
def proxy_add():
    try:
        resp = requests.post(f"{BACKEND_URL}/api/items", json=request.json)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Backend is down"}), 503

@app.route('/proxy/items/<id>', methods=['DELETE'])
def proxy_delete(id):
    try:
        resp = requests.delete(f"{BACKEND_URL}/api/items/{id}")
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Backend is down"}), 503

if __name__ == '__main__':
    print(f"Starting Frontend Service on Port 5002 (Talking to {BACKEND_URL})...")
    app.run(debug=True, host='0.0.0.0', port=5002)