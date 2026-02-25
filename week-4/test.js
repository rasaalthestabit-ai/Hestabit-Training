const mongoose = require("mongoose");

const AccountRepository = require("./src/repositories/account.repository");
const OrderRepository = require("./src/repositories/order.repository");

require("dotenv").config({
  path: `.env.${process.env.NODE_ENV || "local"}`
});

async function runTest() {

    try{

        await mongoose.connect(process.env.DB_URI);

        console.log("Database Connected");

        const account = await AccountRepository.create({

            firstName:"John",
            lastName:"Doe",
            email:"john@test.com",
            password:"123456"

        });

        console.log("Account Created:");
        console.log(account);

        const order = await OrderRepository.create({

            accountId: account._id,
            totalAmount: 500

        });

        console.log("Order Created:");
        console.log(order);


        await mongoose.disconnect();

        console.log("Database Disconnected");

    }
    catch(err){

        console.error("Test Failed");
        console.error(err);

    }

}

runTest();
