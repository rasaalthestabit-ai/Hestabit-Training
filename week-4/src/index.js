const startServer = require("./loaders/app");

startServer()
  .then(() => {
    console.log("App initialized");
  })
  .catch((err) => {
    console.error("Startup error:", err);
  });