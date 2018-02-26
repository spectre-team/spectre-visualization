# this should be python:3.6-alpine or slim when spectre-data is published on PIP
FROM python:3.6

VOLUME /data

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN python -m unittest discover

EXPOSE 80

ENV FLASK_APP=api.py
# this should be done e.g. through nginx, not flask module
ENTRYPOINT ["python", "-m", "flask", "run", "-p", "80", "-h", "0.0.0.0"]
