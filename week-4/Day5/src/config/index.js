const dotenv = require("dotenv");
const path = require("path");

const env = process.env.NODE_ENV || "local";

const envFile = `.env.${env}`;

dotenv.config({
  path: path.resolve(process.cwd(), envFile),
});

module.exports = {

  port: process.env.PORT,

  dbUrl: process.env.DB_URL,

  env: env

};
