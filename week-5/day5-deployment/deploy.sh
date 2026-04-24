#!/bin/bash

echo "Starting deployment..."

docker compose -f docker-compose.yml down

docker compose -f docker-compose.yml build

docker compose -f docker-compose.yml up -d

echo "Deployment completed!"

docker ps
