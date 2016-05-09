# Script to run Docker image
# Assuming that you have running RabbitMQ image with name "rabbit"

# This script will copy your curreent directory with source code
# to /src/ folder inside of Docker with Python 3

docker run --rm -it -v $(pwd):/src/ \
           --link rabbit:rabbit python:3 \
           sh -c "cd /src/ && pip install -r requirements.txt && bash"

