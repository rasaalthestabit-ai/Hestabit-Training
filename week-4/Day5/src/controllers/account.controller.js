const accountRepository = require("../repositories/account.repository");

async function createAccount(req,res,next){
  try{

    const account = await accountRepository.create(req.body);

    res.status(201).json(account);

  }catch(err){
    next(err);
  }
}

async function getAccounts(req,res,next){
  try{

    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;

    const accounts = await accountRepository.findPaginated(page,limit);

    res.json(accounts);

  }catch(err){
    next(err);
  }
}

async function getAccountById(req,res,next){
  try{

    const account = await accountRepository.findById(req.params.id);

    res.json(account);

  }catch(err){
    next(err);
  }
}

async function updateAccount(req,res,next){
  try{

    const account = await accountRepository.update(req.params.id,req.body);

    res.json(account);

  }catch(err){
    next(err);
  }
}

async function deleteAccount(req,res,next){
  try{

    const account = await accountRepository.delete(req.params.id);

    res.json(account);

  }catch(err){
    next(err);
  }
}

module.exports={
  createAccount,
  getAccounts,
  getAccountById,
  updateAccount,
  deleteAccount
};