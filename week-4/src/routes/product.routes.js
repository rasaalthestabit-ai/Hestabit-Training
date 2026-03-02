const express = require("express");
const { sendEmailJob } = require("../jobs/email.job");
const router = express.Router();

const ProductController = require("../controllers/product.controller");
const validate = require("../middlewares/validate");
const productValidation = require("../validations/product.validation");


// CREATE PRODUCT
router.post(
  "/",
  validate(productValidation.createProductSchema),
  ProductController.createProduct
);


// GET PRODUCTS
router.get("/", ProductController.getProducts);


// DELETE PRODUCT
router.delete("/:id", ProductController.deleteProduct);


// Debug route
router.get("/test",(req,res)=>{
  res.send("Products route working");
});

router.post("/email", async (req,res)=>{

 await sendEmailJob({
   email: req.body.email
 });

 res.json({
   message:"Email Job Added"
 });

});

module.exports = router;