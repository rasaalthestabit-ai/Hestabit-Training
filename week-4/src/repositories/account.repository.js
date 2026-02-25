const Account = require("../models/Account");

class AccountRepository{


async create(data){

    return await Account.create(data);

}


async findById(id){

    return await Account.findById(id);

}


async findPaginated(page=1,limit=10){

    const skip = (page-1)*limit;

    return await Account.find()

        .skip(skip)

        .limit(limit)

        .sort({
            createdAt:-1
        });

}


async update(id,data){

    return await Account.findByIdAndUpdate(

        id,
        data,
        {
            new:true
        }

    );

}


async delete(id){

    return await Account.findByIdAndDelete(id);

}


}


module.exports = new AccountRepository();
