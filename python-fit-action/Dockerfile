FROM python:3.8

ARG IMAGE_NAME

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY fit_action_example.py /app/fit_action_example.py

WORKDIR /app

ENV IMAGE_NAME="$IMAGE_NAME"

ENTRYPOINT ["python", "fit_action_example.py"]