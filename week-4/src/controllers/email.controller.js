const { sendEmailJob } = require("../jobs/email.job");

async function sendEmail(req, res, next) {
  try {

    const { email } = req.body;

    if (!email) {
      return res.status(400).json({
        success: false,
        message: "Email is required"
      });
    }

    await sendEmailJob({ email });

    res.json({
      success: true,
      message: "Email job added to queue"
    });

  } catch (err) {
    next(err);
  }
}

module.exports = {
  sendEmail
};