const orderRepository = require("../repositories/order.repository");

async function createOrder(req, res, next) {
  try {

    const order = await orderRepository.create(req.body);

    res.status(201).json(order);

  } catch (err) {
    next(err);
  }
}

async function getOrders(req, res, next) {
  try {

    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;

    const orders = await orderRepository.findPaginated(page, limit);

    res.json(orders);

  } catch (err) {
    next(err);
  }
}

async function getOrderById(req, res, next) {
  try {

    const order = await orderRepository.findById(req.params.id);

    res.json(order);

  } catch (err) {
    next(err);
  }
}

async function updateOrder(req, res, next) {
  try {

    const order = await orderRepository.update(req.params.id, req.body);

    res.json(order);

  } catch (err) {
    next(err);
  }
}

async function deleteOrder(req, res, next) {
  try {

    const order = await orderRepository.delete(req.params.id);

    res.json(order);

  } catch (err) {
    next(err);
  }
}


module.exports = {
  createOrder,
  getOrders,
  getOrderById,
  updateOrder,
  deleteOrder
};