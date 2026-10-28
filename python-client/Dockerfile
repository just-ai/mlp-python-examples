FROM python:3.8

ARG IMAGE_NAME

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY client_app_example.py /app/client_app_example.py

WORKDIR /app

ENV IMAGE_NAME="$IMAGE_NAME"

ENTRYPOINT ["python", "client_app_example.py"]