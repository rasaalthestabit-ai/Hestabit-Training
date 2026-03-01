const Joi = require("joi");


const createProductSchema = Joi.object({

 name:Joi.string()
  .min(2)
  .max(50)
  .required(),

 description:Joi.string()
  .max(200)
  .allow(""),

 price:Joi.number()
  .min(1)
  .max(100000)
  .required(),

 tags:Joi.array()
  .items(Joi.string())
  .default([])

});


module.exports = {

 createProductSchema

};
