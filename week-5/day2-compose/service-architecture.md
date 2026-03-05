# Multi-Container Docker Application

## Overview

This project demonstrates a multi-container application using Docker Compose.

The system consists of three services:

- React client (frontend)
- Node.js server (backend API)
- MongoDB database

All services run in isolated containers and communicate through Docker networking.

---

## Architecture

```
Browser
   |
   v
React Client (3000)
   |
   v
Node Server (5000)
   |
   v
MongoDB (27017)
```

---

## Services

### Client

Frontend React application.

- Built using React
- Runs on port 3000
- Communicates with backend API

---

### Server

Node.js backend service.

- Express API
- Runs on port 5000
- Connects to MongoDB using Docker network

Connection string:

```
mongodb://mongo:27017/mydb
```

---

### Database

MongoDB container used for persistent storage.

- Image: mongo:7
- Port: 27017
- Data stored using Docker volumes

---

## Docker Networking

Docker Compose automatically creates a network.

Services communicate using service names:

- client → server
- server → mongo

Example:

```
mongodb://mongo:27017
```

---

## Volumes

MongoDB data is persisted using a Docker volume.

```
mongo-data:/data/db
```

This ensures database data remains even if containers restart.

---

## Running the Application

Start all services:

```
docker compose up -d
```

Stop services:

```
docker compose down
```

---

## Logs

Logs can be viewed using:

```
docker logs react-client
docker logs node-server
docker logs mongo
```

---

## Key Learnings

- Multi-container applications
- Docker Compose orchestration
- Container networking
- Persistent volumes
- Service isolation
