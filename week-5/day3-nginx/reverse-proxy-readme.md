# NGINX Reverse Proxy + Load Balancing

## Overview

This project demonstrates how to use **NGINX as a reverse proxy and load balancer** for multiple backend services running in Docker containers.

The system consists of:

- NGINX reverse proxy
- Two backend Node.js servers
- Docker Compose for orchestration

---

## Architecture

Client requests first reach the **NGINX container**, which distributes traffic between two backend servers using **round-robin load balancing**.


---

## Reverse Proxy

A **reverse proxy** sits between clients and backend services.

Instead of clients connecting directly to the backend servers, they communicate with NGINX, which forwards the request internally.

Benefits:
- Security
- Load balancing
- Centralized routing
- Scalability

---

## Load Balancing

NGINX distributes incoming requests across multiple backend servers.

This project uses **round-robin load balancing**, which works as follows:

Request 1 → backend1
Request 2 → backend2
Request 3 → backend1
Request 4 → backend2


This ensures traffic is evenly distributed.

---

## NGINX Configuration

The `upstream` block defines backend servers:

```nginx
upstream backend_servers {
  server backend1:3000;
  server backend2:3000;
}
```
The location block routes API requests:

location /api {
  proxy_pass http://backend_servers;
}

## Running the project

Start the containers:

docker compose up -d --build

Check running containers:

docker ps

## Testing Load-Balancing

Open the API endpoint:

http://localhost:8080/api

Refreshing the page shows alternating responses from different backend containers.

Example response:

{
  "message": "Hello from backend",
  "container": "backend1"
}

## Conclusion

This setup demonstrates how NGINX can act as a reverse proxy and load balancer for containerized backend services.

It simulates a simplified production architecture used in scalable web systems.

### Containers running


docker ps

You should see:


backend1
backend2
nginx-proxy

### API works

Open:


http://localhost:8080/api


---

### Load balancing works

Run:


curl localhost:8080/api


Multiple times and check **container alternates**.

---

### Reverse Proxy


Client → NGINX → Backend


---

### Load Balancing

Multiple servers handle traffic.

---

### Docker Service Networking

Containers communicate via **service names**.

---

### Horizontal Scaling

Instead of upgrading a server, you **add more servers**.

---
