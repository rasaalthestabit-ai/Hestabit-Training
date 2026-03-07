#!/bin/bash

echo "Starting deployment..."

docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml build

docker compose -f docker-compose.prod.yml up -d

echo "Deployment completed!"

docker ps
