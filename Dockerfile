# Use the AWS Lambda Python 3.9 base image
FROM public.ecr.aws/lambda/python:3.9

# Set the working directory inside the Lambda environment
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install build tools and dependencies
RUN yum install -y gcc rust cargo && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    yum remove -y gcc rust cargo && \
    yum clean all

# Copy your application code (this layer changes most often)
COPY . .

# Set the CMD to your handler
CMD ["main.lambda_handler"]
