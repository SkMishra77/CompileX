# Setup

1. Install AWS CLI.
2. Configure AWS CLI
```shell
aws configure
```
3. Create ECR Repository
```shell
aws ecr create-repository --repository-name compile-x-cpp --region ap-south-1
```
4. Get the ECR URI
```shell
aws ecr describe-repositories --repository-names compile-x-cpp --region ap-south-1 --query "repositories[0].repositoryUri" --output text
```
5. Build the Docker Image
```shell
docker build -t compile-x-cpp .
```
6. Tag the Docker image:
```shell
docker tag <::ECR URI::>/compile-x-cpp:latest
```
7. Push the Docker image to ECR:
```shell
docker push <::ECR URI::>/compile-x-cpp:latest
```
8. Setup the Lambda Function
```shell
aws lambda create-function \
  --function-name compile-x-cpp \
  --package-type Image \
  --code ImageUri=020867940800.dkr.ecr.ap-south-1.amazonaws.com/compile-x-cpp:latest \
  --memory-size 512 \
  --timeout 20 \
  --ephemeral-storage Size=512 \
  --role arn:aws:iam::<your-account-id>:role/<your-lambda-execution-role> \
  --region ap-south-1
```