StoreManager: Microservices Inventory Application
---

### 📋 Project Overview
This project demonstrates the migration of a monolithic inventory management system into a distributed Microservices Architecture. The application is containerized using Docker and orchestrated using Kubernetes.
It consists of two decoupled services:
Frontend Service: A Flask-based UI that handles user interactions.
Backend Service: A Flask-based REST API that manages inventory data.

---

### 🏗️ Architecture Evolution
Phase 1: The Monolith (Before)
In the initial phase, the application was designed as a single unit where the User Interface (UI), Business Logic, and Data Access all lived inside one process.
Pros: Simple to develop initially.
Cons: Hard to scale individual components; a crash in one part kills the whole app.

    +-------------------------------------------------------+
    |   USER / BROWSER                                      |
    +-----------+-------------------------------------------+
                |
                | HTTP Request
                v
    +-----------+-------------------------------------------+
    |   DOCKER CONTAINER: storemanager                      |
    |                                                       |
    |   +-------------------+    +---------------------+    |
    |   |  Frontend UI      |--->|  Backend API Logic  |    |
    |   +-------------------+    +----------+----------+    |
    |                                       |               |
    |                                       v               |
    |                            +----------+----------+    |
    |                            |   In-Memory Data    |    |
    |                            +---------------------+    |
    +-------------------------------------------------------+
    

Phase 2: Microservices Architecture (After)
The application was refactored into two distinct services running in separate containers. This allows independent scaling and failure isolation.
Frontend Service: Runs on Port 5002. exposed via LoadBalancer.
Inventory Backend: Runs on Port 5001. Internal ClusterIP only.
Communication: HTTP/REST over Kubernetes internal DNS (inventory-service).

                                  Internet
                                     |
                                     v
                           +----------------------+
                           |   LoadBalancer (80)  |
                           +---------+------------+
                                     |
      Kubernetes Cluster             |
    +--------------------------------|----------------------------------+
    |                                v                                  |
    |  +-------------------------------------------------------------+  |
    |  |  Frontend Service (Deployment: store-frontend)              |  |
    |  |                                                             |  |
    |  |   [ Pod: Frontend UI ]  ---(env: INVENTORY_SERVICE_URL)---> |  |
    |  +-------------------------------------------------------------+  |
    |                                |                                  |
    |                                | Internal Call (Port 5001)        |
    |                                v                                  |
    |  +-------------------------------------------------------------+  |
    |  |  Backend Service (Deployment: inventory-backend)            |  |
    |  |  (ClusterIP: inventory-service)                             |  |
    |  |                                                             |  |
    |  |   [ Pod: Backend API ]  <----->  [ In-Memory Data ]         |  |
    |  +-------------------------------------------------------------+  |
    |                                                                   |
    +-------------------------------------------------------------------+

---

### ⚖️ Trade-offs & Analysis
While moving to microservices improved scalability, it introduced specific challenges:
1. Operational Complexity: Managing two services and networking is more complex than a single script.
2. Data Persistence: Currently, data is stored in-memory. If the Backend pod restarts, data is lost.
3. Network Latency: Communication now requires HTTP calls, introducing slight latency compared to direct function calls.

---

### 🚀 How to Run (Deployment Guide)

Follow these steps to deploy the application on a local Kubernetes cluster (Docker Desktop, Minikube, or Kind).
1. Build the Docker Containers
First, package the source code into Docker images. Run these commands from the root directory:
 Build Backend Image
docker build -f Dockerfile.backend -t store-backend:v1 .

 Build Frontend Image
docker build -f Dockerfile.frontend -t store-frontend:v1 .


2. Deploy to Kubernetes
Apply the configuration file to create the Deployments and Services:
kubectl apply -f k8s-deployment.yaml


3. Verify Deployment
Check the status of the pods to ensure they are running:
kubectl get pods
Expected Output: You should see two pods (one for backend, one for frontend) with status Running.


4. Access the Application
Check the services to find the access URL:
kubectl get services

Browser Access: Open http://localhost (or the EXTERNAL-IP listed for frontend-service).
You should see the StoreManager interface where you can Add and Delete items.

---

### 📸 Screenshots

Please refer to the screenshots/ folder in this repository for screenshots of the running application and Kubernetes cluster state.

---

### 🔮 Future Roadmap

To prepare this application for a production environment, the following enhancements are recommended:

1.Persistent Storage: Integrate a database (e.g., PostgreSQL) with PVCs to ensure data survives restarts.

2.Observability: Implement logging (EFK Stack) and monitoring (Prometheus) to track service health.

3.CI/CD Pipeline: Automate builds so pushing code to GitHub automatically updates the cluster.


