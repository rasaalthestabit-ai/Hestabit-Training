const express = require("express");

const router = express.Router();

const ProductController = require("../controllers/product.controller");


// Correct routes

router.post("/", ProductController.createProduct);

router.get("/", ProductController.getProducts);

router.delete("/:id", ProductController.deleteProduct);


// Debug route (optional)

router.get("/test", (req,res)=>{
  res.send("Products route working");
});

module.exports = router;