const helmet = require("helmet");
const cors = require("cors");
const rateLimit = require("express-rate-limit");
const mongoSanitize = require("express-mongo-sanitize");
const xss = require("xss");


function sanitizeObject(obj){

  if(!obj) return;

  Object.keys(obj).forEach(key=>{

    if(typeof obj[key] === "string"){
      obj[key] = xss(obj[key]);
    }

    if(typeof obj[key] === "object" && obj[key] !== null){
      sanitizeObject(obj[key]);
    }

  });

}


function security(app){

  app.use(helmet());

  app.use(cors());

  app.use(rateLimit({
    windowMs: 1*60*1000,
    max: 100,
    message: "Too many requests, try again later!"
  }));

  app.use((req,res,next)=>{

    function clean(obj){

      if(!obj) return;

      Object.keys(obj).forEach(key=>{

        if(key.includes("$") || key.includes(".")){
          delete obj[key];
        }

        if(typeof obj[key] === "object"){
          clean(obj[key]);
        }

      });

    }

    clean(req.body);
    clean(req.params);
    clean(req.query);

    next();

});

  app.use((req,res,next)=>{

    sanitizeObject(req.body);

    sanitizeObject(req.params);

    sanitizeObject(req.query);

    next();

  });

}

module.exports = security;