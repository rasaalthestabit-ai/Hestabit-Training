const winston = require("winston");
const path = require("path");
const fs = require("fs");

const logDir = path.join(__dirname, "../logs");

/*
Ensure logs directory exists
*/
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

/*
Custom log format
Includes:
- timestamp
- level
- message
- requestId (if provided)
- metadata (optional)
*/

const customFormat = winston.format.printf(
  ({ timestamp, level, message, requestId, ...meta }) => {

    let baseLog = `${timestamp} [${level.toUpperCase()}]`;

    if (requestId) {
      baseLog += ` [${requestId}]`;
    }

    baseLog += `: ${message}`;

    /*
    Attach metadata if present
    */
    if (Object.keys(meta).length > 0) {
      baseLog += ` | ${JSON.stringify(meta)}`;
    }

    return baseLog;
  }
);

const logger = winston.createLogger({

  /*
  Log level based on environment
  */
  level: process.env.NODE_ENV === "production" ? "info" : "debug",

  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }), // capture stack traces
    customFormat
  ),

  transports: [

    /*
    Console Logs
    */
    new winston.transports.Console(),

    /*
    Error Logs File
    */
    new winston.transports.File({
      filename: path.join(logDir, "error.log"),
      level: "error"
    }),

    /*
    Combined Logs File
    */
    new winston.transports.File({
      filename: path.join(logDir, "combined.log")
    })

  ]

});

module.exports = logger;