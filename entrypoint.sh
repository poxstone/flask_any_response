#!/bin/sh

# delete nginx default service id use port 80
if [[ "${APP_PORT}" == "80" || "${PROXY_HTTP_PORT}" == "80" || "${PROXY_TCP_PORT}" == "80" ]];then
    echo "" > /etc/nginx/conf.d/default.conf;
fi;
# run nginx
echo "" | awk  -v _port="${PROXY_HTTP_PORT}" '{system("sed -iE \"s#listen 3333;#listen "_port";#gI\" /etc/nginx/sites-enabled/reverse-proxy.conf")}';
echo "" | awk  -v _port="${PROXY_HTTP_PORT}" '{system("sed -iE \"s#listen \\[::\\]:3333;#listen [::]:"_port";#gI\" /etc/nginx/sites-enabled/reverse-proxy.conf")}';
echo "" | awk  -v _host="${PROXY_REDIRECT_HTTP_HOST}"   '{system("sed -iE \"s#proxy_pass http://127.0.0.1:3333;#proxy_pass "_host";#gI\" /etc/nginx/sites-enabled/reverse-proxy.conf")}';
# tcp
echo "" | awk  -v _host="${PROXY_TCP_PORT}"   '{system("sed -iE \"s#listen 4444;#listen "_host";#gI\" /etc/nginx/nginx.conf")}';
echo "" | awk  -v _host="${PROXY_REDIRECT_TCP_HOST}"   '{system("sed -iE \"s#server 127.0.0.1:8080;#server "_host";#gI\" /etc/nginx/nginx.conf")}';
nohup nginx &

# normal path
cd $APP_PATH;
# run udp and gunicorn
sleep "${INIT_APP_TIME}";
python3 ./UDP/application.py & \
python3 ./WEBSOCKET/websocket.py & \
# python3 ./GCP_PROFILER/bench.py & \
gunicorn --workers=$WORKERS --timeout=$TIMEOUT --bind 0.0.0.0:$APP_PORT $GUNICORN_MODULE:$GUNICORN_CALLABLE;