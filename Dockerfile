# Using lightweight alpine image
FROM python:2.7-alpine

ENV RUNNING_IN_DOCKER Yes

# Installing packages
RUN apk update
RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY server ./server

# Install dependencies
RUN pipenv install

# Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
