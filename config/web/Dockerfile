# Dockerfile
# stage 1
FROM python:3.12-alpine3.20 AS builder
WORKDIR /home/app/web
# Set environment variables
# prevent python from writing pyc files to disc, equivalent to python -B option
ENV PYTHONDONTWRITEBYTECODE 1
# prevents python from buffering stdout and stderr (equivalent to python -u option
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && rm -rf /var/cache/apk/*

# stage 2
FROM python:3.12-alpine3.20
WORKDIR /home/app/web
# copy only the necessary parts from the builder stage
COPY --from=builder /install /usr/local
COPY . .

RUN addgroup --system app && adduser -S app -G app \
    && chmod +x /home/app/web/config/web/server-entrypoint.sh \
    && chown -R app:app /home/app/web \
    && mkdir -p /home/app/web/logs \
    && chmod -R 777 /home/app/web/logs
# change to the app user
USER app