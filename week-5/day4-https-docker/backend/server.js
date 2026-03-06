const http = require("http");

const server = http.createServer((req, res) => {
  res.end("Hello from backend over HTTPS via NGINX!");
});

server.listen(3000, () => {
  console.log("Backend running on port 3000");
});
