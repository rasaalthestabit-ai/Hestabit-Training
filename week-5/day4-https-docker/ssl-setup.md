# SSL Setup with NGINX and Docker

This implementation ensures that:

* All HTTP traffic is redirected to HTTPS
* SSL/TLS encryption is enabled
* Requests are securely proxied to the backend service

---

# Generating SSL Certificates

To enable HTTPS locally, **self-signed certificates** were generated using `mkcert`.

### Install mkcert

```bash
sudo apt install mkcert
```

Install the local certificate authority:

```bash
mkcert -install
```

### Generate certificates for localhost

```bash
mkdir certs

mkcert -key-file certs/localhost-key.pem \
-cert-file certs/localhost.pem \
localhost
```

This creates:

```
certs/
├── localhost.pem
└── localhost-key.pem
```

These certificates are used by NGINX to serve HTTPS.

---

# NGINX HTTPS Configuration

NGINX is configured to:

1. Redirect **HTTP → HTTPS**
2. Use the generated SSL certificates
3. Forward requests to the backend service


### Key Points

**HTTP Redirect**

```
listen 80
```

All HTTP requests are redirected to HTTPS.

```
return 301 https://$host$request_uri;
```

---

**HTTPS Server**

```
listen 443 ssl
```

This enables SSL/TLS.

Certificates used:

```
ssl_certificate /etc/nginx/certs/localhost.pem
ssl_certificate_key /etc/nginx/certs/localhost-key.pem
```

---

**Reverse Proxy**

Requests are forwarded to the backend container:

```
proxy_pass http://backend;
```

---

# Docker Integration

The certificates and configuration are mounted into the NGINX container using Docker volumes.

Example:

```yaml
nginx:
  image: nginx
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
    - ./certs:/etc/nginx/certs
```

This allows NGINX inside Docker to access the SSL certificates and configuration file.

---

# Running the Setup

Start the containers:

```bash
docker compose up --build
```

Verify running containers:

```bash
docker ps
```

---

# Testing HTTPS

### Test using curl

```bash
curl -k https://localhost
```

Expected response:

```
Hello from backend over HTTPS via NGINX!
```

---

### Test in Browser

Open:

```
https://localhost
```

The browser should connect securely and display the backend response.

---

# HTTP to HTTPS Redirect

Accessing:

```
http://localhost
```

automatically redirects to:

```
https://localhost
```

This ensures that all traffic is encrypted.

---

# Result

The final setup provides:

* HTTPS enabled using self-signed certificates
* Automatic HTTP → HTTPS redirection
* NGINX acting as a secure reverse proxy
* Backend service accessible over HTTPS

This demonstrates how SSL termination can be implemented in a containerized environment.
