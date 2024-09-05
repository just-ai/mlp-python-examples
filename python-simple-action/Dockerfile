FROM python:3.8

ARG IMAGE_NAME

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY simple_action_example.py /app/simple_action_example.py
WORKDIR /app

ENV IMAGE_NAME="$IMAGE_NAME"

ENTRYPOINT ["python", "simple_action_example.py"]