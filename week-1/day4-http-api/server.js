const http = require('http');

let counter = 0;

const server = http.createServer((req, res) => {

  if (req.url === '/ping') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      timestamp: new Date().toISOString()
    }));
  }

  else if (req.url === '/headers') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(req.headers, null, 2));
  }

  else if (req.url === '/count') {
    counter++;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      count: counter
    }));
  }

  else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Route not found' }));
  }

});

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});
