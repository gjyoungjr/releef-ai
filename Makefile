.EXPORT_ALL_VARIABLES:

AWS_PROFILE=rekha-ai
FRONTEND_DIR := packages/frontend
BACKEND_DIR := packages/backend
REGION := us-east-2
ECR_REPO=public.ecr.aws/y9j1k7y7
IMAGE_NAME=releef-agents
VERSION=1.0.0

## docker run -p 8000:8000 esgene-rag  

# Build and push docker image to ECR 
docker-login:
	aws  ecr-public get-login-password --region us-east-1 --profile ${AWS_PROFILE} | docker login --username AWS --password-stdin public.ecr.aws

docker-build: 
	docker build -f ./Dockerfile -t ${IMAGE_NAME} .

docker-tag: 
	docker tag ${IMAGE_NAME}:latest ${ECR_REPO}/${IMAGE_NAME}:${VERSION}

docker-push: 
	docker push ${ECR_REPO}/${IMAGE_NAME}:${VERSION}

# Full deploy commands
docker-deploy: docker-login docker-build docker-tag docker-push

# CDK commands
cdk-deploy:
	cd infra && cdk deploy --profile ${AWS_PROFILE} --require-approval never

cdk-bootstrap:
	cd infra && cdk bootstrap --profile ${AWS_PROFILE}

# curl http://127.0.0.1:8000/query?query=What%20is%20apple%20doing%20to%20ensure%20net%20zero%20emissions%20by%202030?&index_name=esgeneindex

