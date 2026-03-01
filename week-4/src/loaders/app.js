const security = require("../middlewares/security");
const express = require("express");

const config = require("../config");
const logger = require("../utils/logger");

const connectDB = require("./db");

const productRoutes = require("../routes/product.routes");
const errorMiddleware = require("../middlewares/error.middleware");


async function startServer() {

  const app = express();


  /*
  2️⃣ Load Middlewares
  */

  app.use(express.json({limit:"10kb"}));

  security(app);

  logger.info("Middlewares loaded");


  /*
  1️⃣ Root Test Route
  */

  app.get("/", (req, res) => {
    console.log("ROOT ROUTE HIT");
    res.send("SERVER WORKING");
  });


  /*
  3️⃣ Request Debugger
  */

  app.use((req,res,next)=>{
    console.log("Request:",req.method,req.url);
    next();
  });


  /*
  4️⃣ Connect Database
  */

  await connectDB();


  /*
  5️⃣ Mount Routes
  */

  app.use("/products", productRoutes);

  logger.info("Routes mounted: Product endpoints");


  /*
  6️⃣ Error Middleware
  */

  app.use(errorMiddleware);


  /*
  7️⃣ Start Server
  */

  const server = app.listen(config.port, () => {

    logger.info(`Server started on port ${config.port}`);

  });


  /*
  8️⃣ Graceful Shutdown
  */

  if (!process.listenerCount("SIGINT")) {

    process.on("SIGINT", () => {

      logger.info("Graceful shutdown initiated");

      server.close(() => {

        logger.info("Server closed");

        process.exit(0);

      });

    });

  }

  return app;

}

module.exports = startServer;