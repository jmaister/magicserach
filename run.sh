#!/bin/sh

git pull
pkill -SIGTERM gunicorn
source magicsearch/bin/activate
#export FLASK_APP=app
#export FLASK_ENV=production
nohup gunicorn -b "127.0.0.1:5000" --timeout 60 --workers 2 --reload app:app >> ms.log &

echo Waiting 5 seconds...
sleep 5

echo Running rules engine...
curl 127.0.0.1:5000/runrules
echo

