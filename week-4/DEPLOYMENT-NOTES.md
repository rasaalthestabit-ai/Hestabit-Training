# DEPLOYMENT NOTES

## 1. Project Overview

This project is a Node.js backend API built using:

- Express.js  
- MongoDB  
- Redis  
- BullMQ (for background job processing)  
- Centralized error handling  
- Structured logging  
- Environment-based configuration  

The application follows a production-style architecture:

- The API server handles HTTP requests.
- A separate worker process handles background jobs.
- Redis acts as the message broker.
- MongoDB stores application data.

---

## 2. System Requirements

Ensure the following are installed on your system:

- Node.js (v18 or above recommended)
- npm (comes with Node.js)
- MongoDB (running locally or accessible via URI)
- Redis Server (running locally)

---

## 3. Installation Steps

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <project-folder>
```

### Step 2: Install Dependencies

```bash
npm install
```

---

## 4. Environment Configuration

Create a `.env.local` file in the root directory with the following configuration:

```
PORT=5000
NODE_ENV=local
MONGO_URI=mongodb://localhost:27017/products
REDIS_HOST=localhost
REDIS_PORT=6379
```

Ensure MongoDB and Redis are running before starting the application.

---

## 5. Running the Application

### Step 1: Start MongoDB

If installed locally:

```bash
mongod
```

---

### Step 2: Start Redis

On Linux:

```bash
sudo service redis-server start
```

Or alternatively:

```bash
redis-server
```

---

### Step 3: Start the API Server

```bash
node src/index.js
```

The server will start at:

```
http://localhost:5000
```

---

### Step 4: Start the Background Worker

Open a new terminal window and run:

```bash
node src/workers/email.worker.js
```

The worker listens to Redis and processes background jobs (e.g., email tasks).

**Important:** Both the API server and the worker process must be running for complete functionality.

---

## 6. API Testing

The project includes a Postman collection file:

```
postman_collection.json
```

To test the APIs:

1. Open Postman Desktop App.
2. Import `postman_collection.json`.
3. Create an environment variable:

```
baseUrl = http://localhost:5000
```

4. Run the available endpoints.

---
## 7. Logs

Application logs are stored inside the `/logs` directory.

Logs include:

- Application logs
- Error logs
- Structured logs with request IDs for tracing and debugging

---

## 8. Architecture Summary

- Express handles HTTP requests.
- Controllers manage request flow.
- Services contain business logic.
- MongoDB stores persistent data.
- Redis acts as a job queue broker.
- BullMQ manages background job processing.
- A separate worker consumes and processes queued jobs.
- Centralized error middleware ensures consistent error responses.

---

## 9. Important Notes

- MongoDB must be running for database operations.
- Redis must be running for background job processing.
- API server and worker must both be active.
- Environment variables must be correctly configured before starting the application.
