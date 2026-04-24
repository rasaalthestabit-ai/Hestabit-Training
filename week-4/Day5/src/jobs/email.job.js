const { Queue } = require("bullmq");

const connection = {
  host: "127.0.0.1",
  port: 6379
};

const emailQueue = new Queue("emailQueue", {
  connection
});


async function sendEmailJob(data) {

  await emailQueue.add(
    "sendEmail",

    data,

    {
      attempts: 3,

      backoff: {
        type: "exponential",
        delay: 2000
      }
    }

  );

}

module.exports = {
  sendEmailJob
};
