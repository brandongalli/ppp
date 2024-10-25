# pull official base image
FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-dev iputils-ping \
    default-libmysqlclient-dev \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# set working directory
WORKDIR /app

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r  requirements.txt

# add app
COPY . .
# Set executable permission for the wait-for.sh script


EXPOSE 8080
