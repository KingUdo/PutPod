# set base image (host OS)
FROM python:3.9-slim

#update
RUN apt-get -y update && apt-get -y upgrade

# add putpod user
RUN useradd -ms /bin/bash putpod

# add new group
RUN addgroup --gid 1024 mygroup
RUN usermod -a -G 1024 putpod

USER putpod

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY src/requirements.txt .

# install dependencies
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/* ./
COPY src/objects/ ./objects/
COPY src/misc/ ./misc/

HEALTHCHECK --interval=120s --timeout=15s --start-period=60s CMD curl -L 'http://localhost:8080/'

# command to run on container start
CMD python main.py
