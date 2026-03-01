const mongoose = require("mongoose");
const config = require("./src/config");

const Account = require("./src/models/Account");
const Order = require("./src/models/Order");

async function runTest() {

  try {

    await mongoose.connect(config.dbUrl);

    console.log("Database connected");


    /*
    Create Account
    */

    const account = await Account.create({

      firstName: "Rasaal",
      lastName: "Tewari",
      email: "rasaal@test.com",
      password: "123456"

    });

    console.log("Account Created:");
    console.log(account);


    /*
    Create Order
    */

    const order = await Order.create({

      accountId: account._id,

      amount: 500,

      items: [
        {
          name: "Laptop",
          price: 500,
          quantity: 1
        }
      ]

    });

    console.log("Order Created:");
    console.log(order);


    process.exit();

  } catch (error) {

    console.error(error);

    process.exit(1);

  }

}

runTest();
