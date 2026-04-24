const mongoose = require("mongoose");
const config = require("../config");
const logger = require("../utils/logger");

async function connectDB() {

  try {

    await mongoose.connect(config.dbUrl,{
      serverSelectionTimeoutMS: 5000
    });

    logger.info("Database connected");

  } catch (error) {

    logger.error("Database connection failed");

    console.log(error);

    process.exit(1);

  }

}

module.exports = connectDB;