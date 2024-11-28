#!/bin/bash

# Set variables
AWS_REGION=eu-west-1
AWS_ACCOUNT_ID=704533066374
ECR_REPO_NAME=developer-feedback
ECR_REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"

# Authenticate with ECR
aws ecr get-login-password --region ${AWS_REGION} | \
finch login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Build image with platform specification
finch build --platform linux/amd64 -t ${ECR_REPO_NAME}:latest .

# Tag image
finch tag ${ECR_REPO_NAME}:latest ${ECR_REPO_URI}:latest

# Push image
finch push ${ECR_REPO_URI}:latest

echo "Successfully pushed AMD64 image to ECR: ${ECR_REPO_URI}:latest"
