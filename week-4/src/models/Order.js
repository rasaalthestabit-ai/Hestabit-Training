const mongoose = require("mongoose");

const OrderSchema = new mongoose.Schema(

{

    accountId:{
        type: mongoose.Schema.Types.ObjectId,
        ref:"Account",
        required:true
    },

    totalAmount:{
        type:Number,
        required:true,
        min:0
    },

    status:{
        type:String,
        enum:["pending","completed","cancelled"],
        default:"pending"
    },


    expiresAt:{
        type:Date,
        index:{
            expires:0
        }
    }

},
{
    timestamps:true
}

);


OrderSchema.index({

    status:1,
    createdAt:-1

});


module.exports = mongoose.model(

    "Order",
    OrderSchema

);
