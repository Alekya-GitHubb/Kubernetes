import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so the frontend (or browser) can talk to this from a different port
CORS(app) 

# --- DATA STORAGE (Backend Only) ---
inventory = [
    {"id": "1", "name": "Laptop", "quantity": 10, "price": 999.99},
    {"id": "2", "name": "Mouse", "quantity": 50, "price": 19.99},
    {"id": "3", "name": "Monitor", "quantity": 20, "price": 199.99}
]

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(inventory)

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = {
        "id": str(uuid.uuid4()),
        "name": data.get('name'),
        "quantity": data.get('quantity'),
        "price": data.get('price')
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route('/api/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    inventory = [i for i in inventory if i['id'] != item_id]
    return jsonify({"success": True})

if __name__ == '__main__':
    # Run Backend on Port 5001
    print("Starting Backend Service on Port 5001...")
    app.run(debug=True, host='0.0.0.0', port=5001)