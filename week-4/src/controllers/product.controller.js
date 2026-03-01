const productService = require("../services/product.service");


// CREATE

async function createProduct(req,res,next){

 try{

   const product = await productService.createProduct(req.body);

   res.json(product);

 }catch(err){

   next(err);

 }

}


// GET

async function getProducts(req,res,next){

 try{

   const products = await productService.getProducts(req.query);

   res.json(products);

 }catch(err){

   next(err);

 }

}


// DELETE

async function deleteProduct(req,res,next){

 try{

   const product = await productService.deleteProduct(req.params.id);

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