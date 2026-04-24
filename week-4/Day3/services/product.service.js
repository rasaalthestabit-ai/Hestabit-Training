const Product = require("../models/Product");
const ApiError = require("../utils/AppError");


// CREATE PRODUCT

async function createProduct(data){

  const product = await Product.create(data);

  return product;

}
async function getProducts(query){

  const {
    search,
    minPrice,
    maxPrice,
    sort,
    tags,
    page = 1,
    limit = 10,
    includeDeleted
  } = query;


  const filter = {};


// Soft Delete Filter

if(!includeDeleted){
  filter.deletedAt = null;
}


// Search Engine

if(search){

filter.$or = [

{ name: { $regex: search, $options: "i"}},

{ description: { $regex: search, $options: "i"}}

];

}


// Price Filter

if(minPrice || maxPrice){

filter.price = {};

if(minPrice) filter.price.$gte = Number(minPrice);

if(maxPrice) filter.price.$lte = Number(maxPrice);

}


// Tags Filter

if(tags){

const tagArray = tags.split(",");

filter.tags = { $in: tagArray };

}


// Sorting

let sortOption = { createdAt: -1 };

if(sort){

const [field, order] = sort.split(":");

sortOption = {};

sortOption[field] = order === "desc" ? -1 : 1;

}


// Pagination

const skip = (page-1)*limit;


const products = await Product.find(filter)
.sort(sortOption)
.skip(skip)
.limit(Number(limit));


return products;

}
async function deleteProduct(id){

const product = await Product.findById(id);

if(!product){

throw new ApiError("Product not found","NOT_FOUND",404);

}

product.deletedAt = new Date();

await product.save();

return product;

}
module.exports = {
createProduct,
getProducts,
deleteProduct
};
