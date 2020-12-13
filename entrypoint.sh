#!/bin/sh

cd $APP_PATH;
# run udp and gunicorn
python3 ./UDP/main.py & \
gunicorn --workers=$WORKERS --timeout=$TIMEOUT --bind 0.0.0.0:$APP_PORT $GUNICORN_MODULE:$GUNICORN_CALLABLE;