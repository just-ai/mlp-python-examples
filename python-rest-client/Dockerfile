FROM python:3.8

ARG IMAGE_NAME

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY rest_client_example.py /app/rest_client_example.py
WORKDIR /app

ENV IMAGE_NAME="$IMAGE_NAME"

ENTRYPOINT ["python", "rest_client_example.py"]