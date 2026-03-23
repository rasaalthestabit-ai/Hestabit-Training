const { Worker } = require("bullmq");
const logger = require("../utils/logger");

const connection = {
  host: "127.0.0.1",
  port: 6379
};

const worker = new Worker(
  "emailQueue",
  async job => {

    logger.info(`Processing email job for ${job.data.email}`);

    await new Promise(resolve => setTimeout(resolve, 2000));

    logger.info(`Email sent to ${job.data.email}`);

  },
  { connection }
);

module.exports = worker;