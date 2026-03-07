const express = require("express");

const app = express();

app.get("/", (req, res) => {
  res.send("Hello from backend via HTTPS reverse proxy!");
});

app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

const PORT = process.env.APP_PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
