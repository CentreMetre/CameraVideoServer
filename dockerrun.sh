#!/bin/bash

IMAGE="centremetre/camera-server:latest"
CONTAINER="camera-server"

# Pull the latest image
if docker pull "$IMAGE"; then
    echo "Image pulled successfully."

    # Remove existing container if it exists
    docker rm -f "$CONTAINER" 2>/dev/null

    # Run the container
    docker run -it \
        --name "$CONTAINER" \
        -v myapp-logs:/app/logs \
        -v myapp-files:/app/files \
        -p 5000:8000 \
        -e CAMERA_SD_URL="http://192.168.0.40/sd/"
        "$IMAGE"
else
    echo "Failed to pull image. Exiting."
    exit 1
fi