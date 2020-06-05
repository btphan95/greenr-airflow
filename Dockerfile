FROM python:3.6-slim-stretch

RUN apt update
RUN apt install -y python3-dev gcc

ADD requirements.txt requirements.txt

# Install required libraries
RUN pip install -r requirements.txt

EXPOSE 8008 8080

# Run it once to trigger resnet download
CMD ["airflow", "initdb"]
CMD ["cd", "airflow"]
CMD ["airflow", "scheduler"]
CMD ["airflow", "webserver"]

# Start the server
# CMD ["python", "app.py", "serve"]