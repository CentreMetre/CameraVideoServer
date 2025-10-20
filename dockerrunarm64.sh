#!/bin/bash

IMAGE="centremetre/camera-server:latest-arm64"
CONTAINER="camera-server"

# Pull the latest image
if docker pull "$IMAGE"; then
    echo "Image pulled successfully."
    docker rm -f "$CONTAINER" 2>/dev/null
else
    echo "Failed to pull image. Checking for local image..."
    if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
        echo "No local image found. Exiting."
        exit 1
    fi
fi

docker run -it \
    --name "$CONTAINER" \
    -v camera-server-logs:/app/logs \
    -v camera-server-files:/app/files \
    -p 5000:8000 \
    -e CAMERA_SD_URL="http://192.168.0.40/sd/" \
    "$IMAGE"
