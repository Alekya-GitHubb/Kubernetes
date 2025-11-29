StoreManager: Microservices Inventory Application

---

### 📋 Overview

This assignment demonstrates the migration of a monolithic inventory management system into a distributed Microservices Architecture. The application is containerized using Docker and orchestrated using Kubernetes.

It consists of two decoupled services:

Frontend Service: A Flask-based UI that handles user interactions.

Backend Service: A Flask-based REST API that manages inventory data.

---

### 🏗️ Architecture

The application uses a split architecture where the Frontend acts as a proxy client to the Backend.

Frontend Service: Runs on Port 5002. exposed via LoadBalancer.

Inventory Backend: Runs on Port 5001. Internal ClusterIP only.

Communication: HTTP/REST over Kubernetes internal DNS (inventory-service).

Technologies Used:

Python 3.9

Flask & Flask-CORS

Docker

Kubernetes (k8s)

---

### 📂 Project Structure

| **File** | **Description** | 
| :--- | :--- |
| `Frontend.py` | Source code for the User Interface service. | 
| `Backend_api.py` | Source code for the Inventory Data API. | 
| `Dockerfile.frontend` | Instructions to build the Frontend Docker image. | 
| `Dockerfile.backend` | Instructions to build the Backend Docker image. | 
| `k8s-deployment.yaml` | Kubernetes configuration for Deployments and Services. | 
| `requirements.txt` | Python dependencies (Flask, requests, etc.). | 
| `Architecture_Report.md` | Detailed documentation of the architectural evolution. |

---

### 🚀 How to Run (Deployment Guide)

Follow these steps to deploy the application on a local Kubernetes cluster (Docker Desktop, Minikube, or Kind).

1. Build the Docker Images

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

### 🧪 API Endpoints

While the UI is the main entry point, the Backend API supports the following routes internally:

GET /api/items - Retrieve all inventory items.

POST /api/items - Add a new item.

DELETE /api/items/<id> - Remove an item.
