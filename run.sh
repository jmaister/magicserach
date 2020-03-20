#!/bin/sh

git pull
pkill -SIGTERM flask
source magicsearch/bin/activate
export FLASK_APP=app
export FLASK_ENV=production
nohup flask run -h 127.0.0.1 -p 5000 --with-threads --reload >> ms.log &

sleep 5
curl 127.0.0.1:5000/runrules
