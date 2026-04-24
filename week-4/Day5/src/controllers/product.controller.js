const productService = require("../services/product.service");
const logger = require("../utils/logger");

async function createProduct(req,res,next){

 try{

   logger.info("Creating product", {
     requestId: req.requestId,
     body: req.body
   });

   const product = await productService.createProduct(req.body);

   logger.info("Product created successfully", {
     requestId: req.requestId,
     productId: product._id
   });

   res.json(product);

 }catch(err){
   next(err);
 }

}


async function getProducts(req,res,next){

 try{

   logger.info("Fetching products", {
     requestId: req.requestId,
     query: req.query
   });

   const products = await productService.getProducts(req.query);

   logger.info("Products fetched successfully", {
     requestId: req.requestId,
     count: products.length
   });

   res.json(products);

 }catch(err){
   next(err);
 }

}

async function deleteProduct(req,res,next){

 try{

   logger.info("Deleting product", {
     requestId: req.requestId,
     productId: req.params.id
   });

   const product = await productService.deleteProduct(req.params.id);

   logger.info("Product deleted", {
     requestId: req.requestId
   });

   res.json(product);

 }catch(err){
   next(err);
 }

}


module.exports = {
 createProduct,
 getProducts,
 deleteProduct
};