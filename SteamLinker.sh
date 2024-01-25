#!/bin/sh

envsubst < config.py.tmpl > config.py

python SteamLinker.py