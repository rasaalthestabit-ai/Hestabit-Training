const express = require("express");
const config = require("../config");
const logger = require("../utils/logger");
const fs = require("fs");
const path = require("path");

const initApp = () => {
  const app = express();

  app.use(express.json());
  logger.info("Middlewares loaded");

  // Loading all paths from src/routes
  const routesPath = path.join(__dirname, "../routes");
  fs.readdirSync(routesPath)
    .filter(file => file.endsWith(".js"))
    .forEach(file => {
      const router = require(path.join(routesPath, file));
      app.use(router);
    });

  // Counting all endpoints
  const routeCount = app._router?.stack
    ? app._router.stack.filter(r => r.route && r.route.path).length
    : 0;
  logger.info(`Routes mounted: ${routeCount} endpoints`);

  // Starting server
  const port = config.server.port;
  app.listen(port, () => {
    logger.info(`Server started on port ${port}`);
  });

  return app;
};

module.exports = initApp;
