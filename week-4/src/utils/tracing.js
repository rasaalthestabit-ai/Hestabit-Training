const { v4: uuidv4 } = require("uuid");

function requestTracing(req, res, next) {

  const requestId = uuidv4();

  req.requestId = requestId;

  res.setHeader("X-Request-ID", requestId);

  next();

}

module.exports = requestTracing;
