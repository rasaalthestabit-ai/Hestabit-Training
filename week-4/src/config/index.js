const path = require("path");
const fs = require("fs");
const dotenv = require("dotenv");

const env = process.env.NODE_ENV || "local";
const envFilePath = path.resolve(process.cwd(), `.env.${env}`);
if(!fs.existsSync(envFilePath)){
    console.error(`Config file .env.${env} not found`);
    process.exit(1);
}
dotenv.config({path : envFilePath});
console.log(`Loaded environment: ${env}`);

const requiredVars = ["PORT", "DB_HOST", "DB_PORT", "DB_NAME"];

requiredVars.forEach((key) => {
    if(!process.env[key]){
        console.error(`Missing required environment variable: ${key}`);
        process.exit(1);
    }
});

const config = {
    env,
    server : {
        port : Number(process.env.PORT)
    },
    database : {
        host : process.env.DB_HOST,
        port : Number(process.env.DB_PORT),
        name : process.env.DB_NAME
    }
};

module.exports = config;