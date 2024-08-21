FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add --no-cache --virtual .build-deps \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev libc-dev \
    postgresql-dev ffmpeg

RUN adduser -D -u 1000 -g 1000 my-user

# Ensure the directory exists and has the correct permissions
RUN mkdir -p /my-user/logs \
    && chown -R my-user:my-user /my-user/logs \
    && chmod -R 755 /my-user/logs

# Now create the log file with correct ownership and permissions
RUN touch /my-user/logs/error.log \
    && chown my-user:my-user /my-user/logs/error.log \
    && chmod 644 /my-user/logs/error.log

RUN chmod -R 775 /my-user/logs

RUN mkdir -p /my-user/logs \
    && touch /my-user/logs/error.log \
    && chown -R my-user:my-user /my-user/logs \
    && chmod -R 775 /my-user/logs


ENV APP_DIR /home/my-user
ENV HOME /home/my-user

ENV PATH "$PATH:/home/my-user/.local/bin"

USER my-user

WORKDIR /my-user

ADD requirements.txt my-user/

RUN --mount=type=cache,target=/root/.cache \
    pip install -r my-user/requirements.txt

COPY ./ /my-user
