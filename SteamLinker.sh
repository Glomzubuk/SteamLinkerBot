#!/bin/sh

envsubst < config.py.tmpl > config.py

python main.py