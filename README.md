
# Setup

## Environment

    sudo apt install python3-venv
    sudo apt install python3-flask


    python3 -m venv magicsearch


    pip install -r requirements.txt
    python -m spacy download en
    wget https://www.mtgjson.com/files/AllPrintings.sqlite
    wget https://www.mtgjson.com/files/StandardCards.json

## Setup on server

    localhost:5000/setup
    localhost:5000/runrules


# Production Run

    pkill -SIGTERM flask
    source magicsearch/bin/activate
    export FLASK_APP=app
    export FLASK_ENV=production
    nohup flask run -h 127.0.0.1 -p 5000 --with-threads --reload >> ms.log &

    tail -f ms.log

# CC

Mana color images "CC BY-NC-SA 2.5" from: https://mtg.gamepedia.com/Numbers_and_symbols


# Libraries

## Select2

https://select2.org/
https://select2.org/configuration/options-api

