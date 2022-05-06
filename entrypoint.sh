#!/bin/sh

cd $APP_PATH;
# run udp and gunicorn
sleep "${INIT_APP_TIME}";
python3 ./UDP/application.py & \
gunicorn --workers=$WORKERS --timeout=$TIMEOUT --bind 0.0.0.0:$APP_PORT $GUNICORN_MODULE:$GUNICORN_CALLABLE;