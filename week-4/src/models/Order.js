const mongoose = require("mongoose");

const orderSchema = new mongoose.Schema(
{

accountId: {
type: mongoose.Schema.Types.ObjectId,
ref: "Account",
required: true
},

amount: {
type: Number,
required: true,
min: 0
},

status: {
type: String,
enum: ["pending","completed","cancelled"],
default: "pending"
},

items: [
{
name: String,
price: Number,
quantity: Number
}
],

createdAt: {
type: Date,
default: Date.now
}

});
orderSchema.index({
status:1,
createdAt:-1
});
module.exports = mongoose.model("Order", orderSchema);
