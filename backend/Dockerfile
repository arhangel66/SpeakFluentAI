FROM python:3.10.2-buster

RUN apt update


WORKDIR /
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the project and set the command to launch the service.test1
COPY . .
ENV ENV='PRODUCTION'
ENV PYTHONPATH=.
CMD python3 main.py

