#!/bin/sh
echo "CONTAINER_TIME_INIT: $(date)";
# If ENTRYPOINT VAR is manual set
if [[ "${ENTRYPOINT}" != "" ]];then
  echo "COMMAND_RUN: -- ${ENTRYPOINT}";
  sh $APP_PATH/script.sh ${ENTRYPOINT} && echo "COMMAND_RUN: FINISHED" || echo "COMMAND_RUN: END_WITH_ERRORS";
  echo "CONTAINER_TIME_END: $(date)";
  exit 0;
fi;

# delete nginx default service id use port 80
if [[ "${PORT}" == "80" || "${PROXY_HTTP_PORT}" == "80" || "${PROXY_TCP_PORT}" == "80" ]];then
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
echo "CONTAINER_TIME_PY_INIT: $(date)";
python3 ./UDP/application.py & \
python3 ./WEBSOCKET/websocket.py & \
python3 ./GRPC/main_server.py & \
# python3 ./GCP_PROFILER/bench.py & \
echo "Run gunicorn";

if [[ "${CERTFILE_CRT}" != "" && "${KEYFILE_TLS}" != "" && -f "${CERTFILE_CRT}" && -f "${KEYFILE_TLS}" ]];then
  echo "Run gunicorn With TLS ${CERTFILE_CRT} - ${KEYFILE_TLS}";
  gunicorn --workers="${WORKERS}" --timeout="${TIMEOUT}" --bind="0.0.0.0:${PORT}" "${GUNICORN_MODULE}:${GUNICORN_CALLABLE}" --certfile="${CERTFILE_CRT}" --keyfile="${KEYFILE_TLS}";
else
  echo "Run gunicorn Without TLS";
  gunicorn --workers="${WORKERS}" --timeout="${TIMEOUT}" --bind="0.0.0.0:${PORT}" "${GUNICORN_MODULE}:${GUNICORN_CALLABLE}";
fi;
echo "CONTAINER_TIME_PY_END: $(date)";