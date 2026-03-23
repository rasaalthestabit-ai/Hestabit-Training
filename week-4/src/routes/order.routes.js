const express = require("express");

const router = express.Router();

const orderController = require("../controllers/order.controller");


// CREATE
router.post("/", orderController.createOrder);


// GET ALL (PAGINATION)
router.get("/", orderController.getOrders);


// GET BY ID
router.get("/:id", orderController.getOrderById);


// UPDATE
router.put("/:id", orderController.updateOrder);


// DELETE
router.delete("/:id", orderController.deleteOrder);


module.exports = router;