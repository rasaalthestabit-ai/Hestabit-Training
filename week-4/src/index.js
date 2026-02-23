require("./config");
const logger = require("./utils/logger");
const connectDB = require("./loaders/db");
const initApp = require("./loaders/app");

const startApp = async () => {
  try {
    await connectDB(); // Waits until DB is ready
    logger.info("Bootstrapping application...");
    initApp(); // Starts Express server
  } catch (err) {
    logger.error("Application failed to start");
    logger.error(err.message);
    process.exit(1);
  }
};

startApp();