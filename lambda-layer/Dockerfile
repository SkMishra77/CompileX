# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.10

RUN yum install -y gcc gcc-c++ make

COPY requirements.txt ${LAMBDA_TASK_ROOT}
# Install any dependencies if needed
RUN pip3 install -r requirements.txt


COPY app.py ${LAMBDA_TASK_ROOT}


CMD ["app.lambda_handler"]
