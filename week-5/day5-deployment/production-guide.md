# Production Deployment Guide

## Overview
This project demonstrates a production-style deployment using Docker Compose,
NGINX reverse proxy, and HTTPS.

## Stack
- Node.js backend
- NGINX reverse proxy
- Docker & Docker Compose

## Features
- Environment variables stored in .env
- Docker volumes for persistent logs
- Health checks for backend service
- Automatic container restart policy
- Log rotation to prevent large logs
- Deployment automation script

## Deployment Steps

1. Clone the repository

2. Configure environment variables
Create .env file:

APP_PORT=3000
NODE_ENV=production

3. Run deployment script

./deploy.sh

## Verify deployment

docker ps

Test API:

curl http://localhost:3000

Test HTTPS:

curl -k https://localhost

## Logs

docker logs backend
docker logs nginx
