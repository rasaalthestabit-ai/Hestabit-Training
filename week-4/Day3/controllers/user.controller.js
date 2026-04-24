const userRepository = require("../repositories/user.repository");


// CREATE USER
async function createUser(req, res, next) {
  try {

    const user = await userRepository.create(req.body);

    res.status(201).json(user);

  } catch (err) {
    next(err);
  }
}


// GET USERS (PAGINATION)
async function getUsers(req, res, next) {
  try {

    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;

    const users = await userRepository.findPaginated(page, limit);

    res.json(users);

  } catch (err) {
    next(err);
  }
}


module.exports = {
  createUser,
  getUsers
};