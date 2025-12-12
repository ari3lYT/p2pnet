#!/bin/bash

# GitHub repository details
REPO="ari3lYT/p2pnet"
GITHUB_TOKEN=""

# SSH private key content
SSH_PRIVATE_KEY=$(cat ~/.ssh/id_ed25519)

# Server details
SERVER_USER="ariel"
SERVER_HOST="185.244.212.194"
SERVER_PATH="/var/www/p2pnet"

# Set GitHub secrets using GitHub CLI
echo "Setting up GitHub secrets for $REPO..."

# Set SSH private key
echo "Setting SSH_PRIVATE_KEY secret..."
gh secret set SSH_PRIVATE_KEY --body "$SSH_PRIVATE_KEY" --repo "$REPO"

# Set server user
echo "Setting SERVER_USER secret..."
gh secret set SERVER_USER --body "$SERVER_USER" --repo "$REPO"

# Set server host
echo "Setting SERVER_HOST secret..."
gh secret set SERVER_HOST --body "$SERVER_HOST" --repo "$REPO"

# Set server path
echo "Setting SERVER_PATH secret..."
gh secret set SERVER_PATH --body "$SERVER_PATH" --repo "$REPO"

echo "GitHub secrets setup completed!"
