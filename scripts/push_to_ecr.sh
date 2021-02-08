#!/usr/bin/env bash

AWS_ACCOUNT="332717896378"
AWS_DEFAULT_REGION="us-west-1"
IMAGE_NAME="airflow"
### ECR - build images and push to remote repository

echo "Building image: $IMAGE_NAME:latest"

sudo docker build --rm -t $IMAGE_NAME:latest .

eval $(aws ecr get-login --no-include-email)

# tag and push image using latest
sudo docker tag $IMAGE_NAME $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_NAME:latest
sudo docker push $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_NAME:latest

# tag and push image with commit hash
COMMIT_HASH="init"
sudo docker tag $IMAGE_NAME $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_NAME:$COMMIT_HASH
sudo docker push $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_NAME:$COMMIT_HASH





aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 332717896378.dkr.ecr.us-west-1.amazonaws.com

