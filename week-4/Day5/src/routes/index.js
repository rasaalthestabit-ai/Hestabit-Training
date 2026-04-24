const express = require("express");

const router = express.Router();

const accountRoutes = require("./account.routes");

router.use("/accounts",accountRoutes);

const orderRoutes = require("./order.routes");

router.use("/orders", orderRoutes);

const emailRoutes = require("./email.routes");

router.use("/email", emailRoutes);

const userRoutes = require("./user.routes");

router.use("/users", userRoutes);

router.get("/health", (req, res) => {

  res.json({
    status: "OK"
  });

});


module.exports = router;
