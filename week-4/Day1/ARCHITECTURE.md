# Backend Bootstrapping Architecture

## Folder Structure

src/
 config/
 loaders/
 models/
 routes/
 controllers/
 services/
 repositories/
 middlewares/
 utils/
 jobs/
 logs/


## Boot Flow

1. Config Loader
Loads environment variables

src/config/index.js


2. Logger Initialization

src/utils/logger.js


3. App Loader

src/loaders/app.js


4. Middlewares Loaded


5. Database Connected

src/loaders/db.js


6. Routes Mounted

src/routes/


7. Server Started


## Environment Isolation

.env.local
.env.dev
.env.prod


## Logging

Using Winston Logger

Console + File Logs


## Graceful Shutdown

SIGINT handler closes server safely
