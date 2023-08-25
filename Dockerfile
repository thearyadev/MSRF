FROM python:3.10-alpine

LABEL org.opencontainers.image.source=https://github.com/thearyadev/msrf
LABEL org.opencontainers.image.description="Docker image for msrf"
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /msrf
COPY . .
RUN apk add chromium-chromedriver
RUN pip install poetry==1.3.2
RUN poetry install

ENV DOCKER_CONTAINERIZED_EXECUTION yes
ENTRYPOINT poetry run python main.py