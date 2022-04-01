FROM python:3.8.10

#set working directory
WORKDIR /usr/src/app

#set environment variables
ENV DOCKER_CONTAINER 1 
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

#install dependencies 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#copy the api_service project
COPY ./api_service .