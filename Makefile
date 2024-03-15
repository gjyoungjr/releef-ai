.EXPORT_ALL_VARIABLES:

AWS_ACCOUNT=654654323576
AWS_PROFILE=perennial
REGION=us-east-1
ECR_REPO=public.ecr.aws/y9j1k7y7
IMAGE_NAME=nucleus


## Terraform commands
tf-init:
	terraform -chdir=infrastructure init

tf-plan:
	terraform -chdir=infrastructure plan

tf-apply:
	terraform -chdir=infrastructure apply -auto-approve

## Build and push docker image to ECR 
docker-login:
	aws  ecr-public get-login-password --region ${REGION} --profile ${AWS_PROFILE} | docker login --username AWS --password-stdin ${ECR_REPO}

docker-build: 
	docker build -f ./Dockerfile -t ${IMAGE_NAME} .

docker-tag: 
	docker tag ${IMAGE_NAME}:latest ${ECR_REPO}/${IMAGE_NAME}:latest

docker-push: 
	docker push ${ECR_REPO}/${IMAGE_NAME}:latest