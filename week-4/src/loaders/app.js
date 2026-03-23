const security = require("../middlewares/security");
const express = require("express");

const config = require("../config");
const logger = require("../utils/logger");

const connectDB = require("./db");
const tracing = require("../utils/tracing");
const productRoutes = require("../routes/product.routes");
const indexRoutes = require("../routes");
const errorMiddleware = require("../middlewares/error.middleware");


async function startServer() {

  const app = express();

  /* Middlewares */
  app.use(express.json({limit:"10kb"}));
  app.use(tracing);
  security(app);

  logger.info("Middlewares loaded");


  /* Root test */

  app.get("/", (req, res) => {
    console.log("ROOT ROUTE HIT");
    res.send("SERVER WORKING");
  });


  app.use((req,res,next)=>{
    logger.info(
      `${req.method} ${req.url}`,
      req.requestId
    );

    next();
  });


  /* Database */

  await connectDB();


  app.use((req,res,next)=>{
    logger.info(`${req.method} ${req.originalUrl}`, {
      requestId: req.requestId
    });
    next();
  });

  /* Routes */

  app.use("/products", productRoutes);
  app.use("/", indexRoutes);
  logger.info("Routes mounted: Product endpoints");

  app.use(errorMiddleware);

  const server = app.listen(config.port, () => {

    logger.info(`Server started on port ${config.port}`);

  });


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