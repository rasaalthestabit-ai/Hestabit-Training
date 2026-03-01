const winston = require("winston");
const path = require("path");

const logDir = path.join(__dirname, "../logs");

const logger = winston.createLogger({

  level: "info",

  format: winston.format.combine(

    winston.format.timestamp(),

    winston.format.printf(({ timestamp, level, message }) => {
      return `${timestamp} [${level.toUpperCase()}]: ${message}`;
    })

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

      filename: `${logDir}/error.log`,
      level: "error",

    }),


    /*
    Combined Logs File
    */

    new winston.transports.File({

      filename: `${logDir}/combined.log`

    })

  ]

});

module.exports = logger;
