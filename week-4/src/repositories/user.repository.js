const User = require("../models/User");

class UserRepository {

  async create(data) {
    return await User.create(data);
  }

  async findPaginated(page = 1, limit = 10) {
    const skip = (page - 1) * limit;

    return await User.find()
      .skip(skip)
      .limit(limit)
      .sort({ createdAt: -1 });
  }

}

module.exports = new UserRepository();