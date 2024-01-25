# syntax=docker/dockerfile:1
FROM python:3

# install envsubst
RUN apt-get update
RUN apt-get install -y gettext-base 

# Discord Bot Token
ENV BOT_TOKEN 'USE env.list TO SPECIFY TOKENS'

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY ./SteamLinker/SteamLinker.py ./
COPY ./SteamLinker/config.py.tmpl ./
COPY ./SteamLinker.sh ./

CMD [ "./SteamLinker.sh" ]
