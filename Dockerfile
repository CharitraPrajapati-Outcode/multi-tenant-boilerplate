FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add --no-cache --virtual .build-deps \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev libc-dev \
    postgresql-dev ffmpeg

RUN adduser -D -u 1000 -g 1000 my-user

# Create the directory if it doesn't exist
RUN mkdir -p /my-project/logs
RUN touch /my-project/logs/error.log
RUN touch /my-project/logs/django_request.log

# Change ownership to the user running the application (replace 'myuser' with the actual user)
RUN chown -R my-user:my-user /my-project/logs

# Set proper permissions
RUN chmod -R 755 /my-project/logs

# Set permissions for the existing log files
RUN chmod 644 /my-project/logs/error.log
RUN chmod 644 /my-project/logs/django_request.log

ENV APP_DIR /home/my-user
ENV HOME /home/my-user

ENV PATH "$PATH:/home/my-user/.local/bin"

USER my-user

WORKDIR /my-project

ADD requirements.txt my-project/

RUN --mount=type=cache,target=/root/.cache \
    pip install -r my-project/requirements.txt

COPY ./ /my-project