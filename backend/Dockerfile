# this Dockerfile won't work on it's own, as it requires there to be a
# mongodb database running, and a corresponding configuration.
# use the docker compose file in the root directory instead.
# if for some reason you want to use this Dockerfile/image on its own,
# uncomment the MONGO_URL line below and insert the relevant information
# (remember that you'll also need to make the mongodb database you use
# available to the Docker containers, possibly by port bindings). 
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# COPY . .

COPY src src
COPY .env .env
COPY main.py main.py
COPY conftest.py conftest.py
COPY pytest.ini pytest.ini

# ENV FLASK_BIND_IP=0.0.0.0
# ENV MONGO_URL=mongodb://dockerUser:dockerPass@mongodb:27017/edutaskDb

CMD [ "python", "./main.py"]
