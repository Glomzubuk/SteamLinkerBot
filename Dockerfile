# syntax=docker/dockerfile:1
FROM python:3.12.2-alpine

# install envsubst
RUN apk add envsubst

# Discord Bot Token
ENV BOT_TOKEN 'USE env.list TO SPECIFY TOKENS'

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY ./SteamLinker.sh ./
COPY ./src/config.py ./config.py.tmpl
COPY ./src/main.py ./

CMD [ "./SteamLinker.sh" ]
