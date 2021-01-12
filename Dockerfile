FROM python:3.7-slim
LABEL maintainer="Naveen Pandey<naveen.pnd@gmail.com>"

# Build dependencies
RUN apt-get update && apt-get install -y python3-dev build-essential libsndfile1

# ARG PIP_EXTRA_INDEX_URL='https://pypi.org/simple'

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Installing requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Adding remaining files
ADD . .

# ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

# add meta-information
ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT
ENV MAX_WORKERS=2

CMD uvicorn --host 0.0.0.0 --port 5000 --workers $MAX_WORKERS mosaic.server:app