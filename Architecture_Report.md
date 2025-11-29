Architecture Report: Scaling StoreManager to Microservices

1. Executive Summary

The objective of this project was to evolve a containerized Python application ("StoreManager") from a monolithic architecture into a scalable, distributed microservices architecture deployed on Kubernetes. This report outlines the architectural transformation, the component breakdown, and the deployment strategy used to achieve scalability.

2. Architecture Phase 1: The Monolith (Before)

In the initial phase, the application was designed as a classic Monolith. A monolithic architecture unifies all aspects of the software—User Interface (UI), Business Logic, and Data Access—into a single executable process.

2.1 Component Structure

Single Container: The entire application ran inside one Docker container (storemanager:latest).

Tightly Coupled Code: The Frontend (HTML generation) and Backend (API routes) lived in a single file (app.py).

Shared Resources: The data storage (in-memory inventory list) was a global variable shared directly by both the UI code and the API code.

2.2 Diagram (Before)

The user interacts directly with the single container, which handles all responsibilities internally.

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


2.3 Limitations

Scaling Issues: To handle more traffic, we would have to replicate the entire container, even if only the UI needed more resources.

Single Point of Failure: A bug in the UI code could crash the entire process, taking down the API and data access with it.

3. Architecture Phase 2: Microservices (After)

In the second phase, the application was refactored into a Microservices Architecture. The monolithic codebase was decoupled into two distinct, independent services: the Frontend Service and the Backend Service.

3.1 Component Breakdown

Service A: The Frontend (UI)

Responsibility: Renders the HTML user interface and accepts user inputs.

Behavior: Acts as a client (proxy). It does not store data. Instead, it makes HTTP calls to the Backend Service to fetch or modify data.

Port: Runs on Port 5002.

Service B: The Inventory Backend (API)

Responsibility: Manages the business logic and the data state (Inventory).

Behavior: Exposes a RESTful API (GET, POST, DELETE) for other services to consume. It is the "Source of Truth" for data.

Port: Runs on Port 5001.

3.2 Diagram (After)

The user interacts with the Frontend, which communicates over the Kubernetes internal network to the Backend.

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


4. Kubernetes Deployment Strategy

To deploy this microservices architecture, we utilized Kubernetes to orchestrate the containers. The deployment consists of four key objects defined in k8s-deployment.yaml.

4.1 Deployments (The "What")

We created two separate Deployment objects to ensure high availability and self-healing.

inventory-backend Deployment: Manages the store-backend:v1 pods. It ensures the API is always running.

store-frontend Deployment: Manages the store-frontend:v1 pods. It contains an Environment Variable (INVENTORY_SERVICE_URL) that tells it where to find the backend.

4.2 Services (The "Networking")

We created two Service objects to handle networking and service discovery.

inventory-service (ClusterIP):

Type: ClusterIP (Internal Only).

Purpose: Gives the Backend a stable internal IP address and DNS name. The Frontend simply calls http://inventory-service:5001 to reach it. This keeps the data secure from the public internet.

frontend-service (LoadBalancer):

Type: LoadBalancer (External).

Purpose: Exposes the Frontend application to the outside world (the User's browser) on Port 80.

5. Architectural Analysis: Trade-offs

While the microservices architecture improves scalability, it introduces specific challenges that were not present in the monolith:

Operational Complexity: Managing two services, networking, and deployment configurations is significantly more complex than running a single script.

Data Persistence: In the current implementation, data is stored in-memory within the Backend pod. If the Backend pod restarts (e.g., during a crash or update), all data is lost.

Network Latency: Communication now requires HTTP calls over the network, which introduces slight latency compared to the direct function calls used in the monolith.

6. Future Roadmap

To prepare this application for a production environment, the following enhancements are recommended:

Persistent Storage: Integrate a database (e.g., PostgreSQL or MongoDB) with Kubernetes PersistentVolumeClaims (PVC) to ensure data survives pod restarts.

Observability: Implement logging (EFK Stack) and monitoring (Prometheus/Grafana) to track the health of individual services.

CI/CD Pipeline: Automate the build and deployment process so that pushing code to GitHub automatically updates the Kubernetes cluster.

7. Conclusion

By moving to this architecture, the StoreManager application is now horizontally scalable. We can now increase the number of Frontend pods (replicas) to handle millions of users without needing to duplicate the Backend data layer, efficiently optimizing resource usage.
