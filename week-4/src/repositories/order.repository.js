const Order = require("../models/Order");

class OrderRepository {

async create(data){

return await Order.create(data);

}


async findById(id){

return await Order.findById(id).populate("accountId");

}


async findPaginated(page=1,limit=10){

const skip=(page-1)*limit;

return await Order.find()
.skip(skip)
.limit(limit)
.sort({createdAt:-1});

}


async update(id,data){

return await Order.findByIdAndUpdate(
id,
data,
{new:true}
);

}


async delete(id){

return await Order.findByIdAndDelete(id);

}

}

module.exports = new OrderRepository();
