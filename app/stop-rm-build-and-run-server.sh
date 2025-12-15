#!/bin/bash

# Stop one or more running containers
docker stop server_ca2_container

# Block until one or more containers stop, then print their exit codes
docker wait server_ca2_container

# Remove one or more containers
docker rm server_ca2_container

# Start a build (image)
docker build . -t sc/server_ca2_image:latest

# Create and run a new container from an image
docker run -d \
	--name server_ca2_container \
	--hostname server_ca2 \
	-p 8080:8080 \
	sc/server_ca2_image:latest
