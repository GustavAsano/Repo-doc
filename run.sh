#!/bin/bash

# Change to script directory
cd "$(dirname "$0")"
echo "heheeeeeeeee $(dirname "$0")"
# Check if docker compose is installed
if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Please install Docker and try again."
    cd - > /dev/null && exit 1
fi

# Parse command line arguments for model value
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --dev) dev="true"; shift ;;
        --down) down="true"; shift ;;
        *) echo "Unknown parameter passed: $1"; cd - > /dev/null && exit 1 ;;
    esac
done

# Stop potentially running containers
echo "Stopping containers..."
docker compose down --remove-orphans 2> /dev/null

# Check if down flag is set (nothind else to do)
if [ "$down" = "true" ]
then
    cd - > /dev/null && exit
fi

# Create cache directory
mkdir -p backend/data/cache

# Check for ssh keys
# if [ ! -f ~/.ssh/id_rsa ] || [ ! -f ~/.ssh/config ]
# then
#     echo "SSH key and configuration not found in ~/.ssh. Please add an SSH key that can access genms-proxy git repository."
#     cd - > /dev/null && exit 1
# fi
# export SSH_CONFIG=$(cat ~/.ssh/config)
# export SSH_PRIVATE_KEY=$(cat ~/.ssh/id_rsa)

# Check secrets file is present
if [ ! -f ".env.secrets" ]
then
    echo ".env.secrets not found. Please create .env.secrets and try again."
    echo "See .env.default_secrets for an example configuration."
    echo "Be mindful of not committing .env.secrets to version control."
    cd - > /dev/null && exit 1
fi

# Choose deployment type
env_file_arg="--env-file .env.secrets_defaults --env-file .env.secrets --env-file .env.defaults"

# Run docker compose
if [ "$dev" = "true" ]
then
    echo "Running in development mode."
    command="docker compose $env_file_arg -f dev.docker-compose.yml up --build --remove-orphans"
    echo "$command"
    eval $command
    cd - > /dev/null && exit
else
    echo "Running in production mode."
    command="docker compose $env_file_arg up --build --remove-orphans -d"
    echo "$command"
    eval $command
    echo "Showing logs (stop reading with Ctrl + C)..."
    docker compose logs -f
    cd - > /dev/null && exit
fi