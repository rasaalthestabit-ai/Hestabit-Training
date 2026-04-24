# Linux Inside Container

## 1. Image Details

docker images
docker history node-day1-docker
docker build -t image_name .

Each Dockerfile instruction creates a layer

"U" indicates image is in use

## 2. Run Container

docker run -d -p 3000:3000 --name day1 day1-container

Detached mode (-d), port mapping (-p), named container

Node app accessible at http://localhost:3000

## 3. Enter Container

docker exec -it day1-container /bin/sh

Interactive shell to explore Linux internals

## 4. File System

pwd
ls -la
cd /app
ls -la
df -h
du -sh /app

Root / contains Linux directories

/app has Node app files

Disk usage shows OverlayFS layered filesystem

## 5. Users & Permissions

whoami
id

Runs as non-root appuser

UID/GID inside container may differ from host

Security best practice

## 6. Processes

ps aux
top

PID 1 → Node server

PID 1 inside container ≠ PID on host (PID namespace)

Shell sessions are additional processes

## 7. Networking

ping 8.8.8.8
ip addr

Container has internet access

eth0 connected via Docker bridge

Network namespace isolation

## 8. Environment Variables

env

NODE_VERSION, HOME, PATH, PWD

Shows runtime and user environment

## 9. Logs(Host)

docker logs day1-container

Shows Node app output

Useful for debugging without entering container

## 10. Inspect Container (Advanced)

docker inspect day1-container
docker inspect --format '{{.State.Pid}}' day1-container
cat /proc/<PID>/cgroup

PID inside container ≠ host PID

Shows cgroups (CPU, memory) and OverlayFS info

## 11. Container Lifecycle

docker stop day1-container
docker rm day1-container

Stops and removes container, freeing resources

