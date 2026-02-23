# Week-4 Backend Architecture

This backend is built with **Node.js + Express + MongoDB** using a **modular, layered architecture**.

## Architecture Overview

src/
config/ # Environment config loader (.env.local/.env.dev/.env.prod)
loaders/ # Bootstrapping: app.js (Express + routes + middleware), db.js (MongoDB connection)
routes/ # Express routes (dynamically loaded)
controllers/ # Handle HTTP requests and send responses
services/ # Business logic (validation, password hashing, email checks)
repositories/ # Database operations (CRUD)
middlewares/ # Express middlewares (JSON parser, auth, logging)
models/ # MongoDB schemas
utils/ # Logger (Winston), helper functions
jobs/ # Background tasks or scheduled jobs
logs/ # Application logs


### Bootstrapping Flow

1. **Load config** → environment variables validated  
2. **Initialize logger** → Winston logs startup steps  
3. **Connect to MongoDB** → async, fail-fast if DB is down  
4. **Initialize Express app** → mount middlewares  
5. **Load & mount routes dynamically** → accurate endpoint count  
6. **Start server** → only after DB and routes are ready  

### Key Principles

- **Single Responsibility**: each layer handles only one concern  
- **Fail-fast**: server won’t start if critical dependencies are missing  
- **Dynamic & modular**: adding a route or middleware is plug-and-play  
- **Environment-driven bootstrapping**: easily switch between local, dev, prod  

