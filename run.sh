#!/bin/sh

git pull
pkill -SIGTERM gunicorn
source magicsearch/bin/activate
#export FLASK_APP=app
#export FLASK_ENV=production
nohup gunicorn -b "127.0.0.1:5000" --timeout 60 --workers 2  app:app >> ms.log &

sleep 5
curl 127.0.0.1:5000/runrules
