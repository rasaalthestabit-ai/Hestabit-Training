const mongoose = require("mongoose");
const config = require("../config");
const logger = require("../utils/logger");



const connectDB = async () => {
    const dbUrl = `mongodb://${config.database.host}:${config.database.port}/${config.database.name}`;

    try{
        await mongoose.connect(dbUrl);
        logger.info(`Database connected : ${config.database.name}@${config.database.host}:${config.database.port}`)
    }
    catch (error){
        logger.error("Database connection failed");
        logger.error(error.message);
        process.exit(1);
    }
};
module.exports = connectDB;