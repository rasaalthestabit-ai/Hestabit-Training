const logger = require("../utils/logger");

module.exports = (err, req, res, next) => {

  const status = err.statusCode || 500;

  /*
  Log the error with requestId and stack
  */
  logger.error(err.message, {
    requestId: req.requestId,
    stack: err.stack,
    path: req.originalUrl,
    method: req.method
  });

  res.status(status).json({
    success: false,
    message: err.message || "Internal Server Error",
    code: err.code || "SERVER_ERROR",
    timestamp: new Date(),
    path: req.originalUrl
  });

};