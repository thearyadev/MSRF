FROM python:3.10-alpine
WORKDIR /msrf
COPY . .
RUN apk add chromium-chromedriver
RUN pip install poetry==1.3.2
RUN poetry install; exit 0
ENTRYPOINT poetry run python main.py