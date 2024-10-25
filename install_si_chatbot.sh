#!/bin/bash

# Exit the script if any command fails
set -e

# Variables that are already set in the environment
FRONTEND_IMAGE_TAG="si-chatbot-fe"
BACKEND_IMAGE_TAG="si-chatbot-be"
DATABASE_VOLUME="database_volume"
LOGGING_VOLUME="logging_volume"
BACKEND_PORT=9508
FRONTEND_PORT=9502

# Function to check if a port is available
check_port() {
    local port=$1
    if ss -tuln | grep -q ":$port "; then
        echo -e "\n\033[31mError:\033[0m Port $port is already in use. Please free the port and rerun the installation."
        exit 1
    fi
}

# Function to check if a container is already running
check_container() {
    local container_name=$1
    if podman ps --filter "name=$container_name" --format "{{.Names}}" | grep -w "$container_name" > /dev/null 2>&1; then
        echo -e "\n\033[31mError:\033[0m Container $container_name is already running. Please stop the container and rerun the installation."
        exit 1
    fi
}

# Divider function for better readability
print_divider() {
    echo -e "\n\033[34m======================================================================================\033[0m\n"
}

# Step 1: Check if ports are available
print_divider
echo -e "\033[36mStep 1: Checking if ports $BACKEND_PORT and $FRONTEND_PORT are available...\033[0m"
check_port $BACKEND_PORT
check_port $FRONTEND_PORT
echo -e "\033[32mSuccess:\033[0m Ports $BACKEND_PORT and $FRONTEND_PORT are available."

# Step 2: Check if containers are running
print_divider
echo -e "\033[36mStep 2: Checking if backend or frontend container is already running...\033[0m"
check_container "backend"
check_container "frontend"
echo -e "\033[32mSuccess:\033[0m No existing backend or frontend containers are running."

# Step 3: Build Docker Images
print_divider
echo -e "\033[36mStep 3: Building Docker image for frontend...\033[0m"
cd frontend/
podman build . --no-cache --pull -f dockerfile.frontend -t $FRONTEND_IMAGE_TAG
print_divider
echo -e "\033[36mBuilding Docker image for backend...\033[0m"
cd ../backend/
podman build . --no-cache --pull -f dockerfile.backend -t $BACKEND_IMAGE_TAG

# Step 4: Create Persistent Volumes
print_divider
echo -e "\033[36mStep 4: Creating persistent volumes...\033[0m"
if podman volume inspect $DATABASE_VOLUME > /dev/null 2>&1; then
    echo -e "\033[33mNotice:\033[0m Volume $DATABASE_VOLUME already exists, skipping creation."
else
    echo -e "\033[32mCreating:\033[0m Persistent volume $DATABASE_VOLUME for database..."
    podman volume create $DATABASE_VOLUME
fi

if podman volume inspect $LOGGING_VOLUME > /dev/null 2>&1; then
    echo -e "\033[33mNotice:\033[0m Volume $LOGGING_VOLUME already exists, skipping creation."
else
    echo -e "\033[32mCreating:\033[0m Persistent volume $LOGGING_VOLUME for logging..."
    podman volume create $LOGGING_VOLUME
fi

# Step 5: Run Backend Container
print_divider
echo -e "\033[36mStep 5: Running backend docker container...\033[0m"
podman run -d --name backend --restart=unless-stopped -p $BACKEND_PORT:$BACKEND_PORT -v $DATABASE_VOLUME:/app/database -v $LOGGING_VOLUME:/app/logging $BACKEND_IMAGE_TAG

# Step 6: Run Frontend Container
print_divider
echo -e "\033[36mStep 6: Running frontend docker container...\033[0m"
podman run -d --name frontend --restart=unless-stopped -p $FRONTEND_PORT:$FRONTEND_PORT $FRONTEND_IMAGE_TAG

# Step 7: Successful setup
print_divider
echo -e "\033[32mSuccess:\033[0m Backend server is now running on port $BACKEND_PORT"
echo -e "\033[32mSuccess:\033[0m Frontend server is now running on port $FRONTEND_PORT"

# Step 8: Frontend UI access
print_divider
echo -e "\033[36mAccess the frontend UI at:\033[0m https://<host>:$FRONTEND_PORT/querius/"
print_divider
