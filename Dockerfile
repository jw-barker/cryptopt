# syntax=docker/dockerfile:1

FROM python:3.9-alpine

WORKDIR /app
COPY cryptopt.py ./
CMD [ "python", "./cryptopt.py"]
