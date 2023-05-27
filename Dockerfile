#FROM alpine:3.16.0
FROM nginx:stable-alpine-perl

ENV PORT='8080'
ENV PROXY_HTTP_PORT='9191'
ENV PROXY_TCP_PORT='9090'
ENV GRPC_PORT='50051'
ENV PROXY_REDIRECT_HTTP_HOST='http://localhost:8080/'
ENV PROXY_REDIRECT_TCP_HOST='localhost:8080'
ENV UDP_PORT='5005'
ENV GUNICORN_MODULE='application'
ENV GUNICORN_CALLABLE='app'
ENV GUNICORN_USER='root'
ENV APP_PATH='/app'
ENV WORKERS='1'
ENV TIMEOUT='120'
ENV INIT_APP_TIME='0'
ENV VERSION_DEP='vp.0.0.2dock'
ENV UDP_PORT='5005'
ENV WEBSOCKET_PORT='5678'
ENV MSSQL_VERSION='17.5.2.1-1'
ENV SLEEP_TIME='0'
ENV LOGS_PRINT='true'
ENV LETS_TOKEN=''
# use it for rewrite ENTRYPOINT='stress-ng --cpu 1 -t 1m --vm-bytes 128M'
ENV CERTFILE_CRT='./.certs/tls.crt'
ENV KEYFILE_TLS='./.certs/tls.key'
ENV CHAIN_PEM='./.certs/chain.pem'

# Change entrypoint
ENV ENTRYPOINT=''

# for gcp Profiler
#ENV GOOGLE_CLOUD_PROJECT=''


RUN apk add --no-cache python3 ca-certificates\
    && apk add nmap mysql-client redis lsblk curl tcpdump tar tmux bind-tools stress-ng vim \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip gunicorn 
#    && adduser -D -h $APP_PATH $GUNICORN_USER

# add gcp profiler
RUN apk add python3-dev ca-certificates gcc build-base\
    && pip3 wheel --wheel-dir=/tmp/wheels google-cloud-profiler \
    && pip3 install --no-index --find-links=/tmp/wheels google-cloud-profiler
    
# sqlcmd sql server client
WORKDIR /tmp
# Installing system utilities
RUN apk add --no-cache curl gnupg --virtual .build-dependencies -- && \
    # Adding custom MS repository for mssql-tools and msodbcsql
    curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_${MSSQL_VERSION}_amd64.apk && \
    curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_${MSSQL_VERSION}_amd64.apk && \
    # Verifying signature
    curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_${MSSQL_VERSION}_amd64.sig && \
    curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_${MSSQL_VERSION}_amd64.sig && \
    # Importing gpg key
    curl https://packages.microsoft.com/keys/microsoft.asc  | gpg --import - && \
    gpg --verify msodbcsql17_${MSSQL_VERSION}_amd64.sig msodbcsql17_${MSSQL_VERSION}_amd64.apk && \
    gpg --verify mssql-tools_${MSSQL_VERSION}_amd64.sig mssql-tools_${MSSQL_VERSION}_amd64.apk && \
    # Installing packages
    echo y | apk add --allow-untrusted msodbcsql17_${MSSQL_VERSION}_amd64.apk mssql-tools_${MSSQL_VERSION}_amd64.apk && \
    # Deleting packages
    apk del .build-dependencies && rm -f msodbcsql*.sig mssql-tools*.apk && \
    ln -s /opt/mssql-tools/bin/sqlcmd /usr/bin/sqlcmd && ln -s /opt/mssql-tools/bin/bcp /usr/bin/bcp; \
    mkdir -p /etc/nginx/sites-enabled/ && mkdir -p /etc/nginx/sites-available/

COPY ./ $APP_PATH

RUN pip3 install -r $APP_PATH/requirements.txt --upgrade

# config nginx
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./nginx/reverse-proxy.conf /etc/nginx/sites-available/reverse-proxy.conf
RUN ln -s /etc/nginx/sites-available/reverse-proxy.conf /etc/nginx/sites-enabled/reverse-proxy.conf

EXPOSE $PORT
EXPOSE $PROXY_HTTP_PORT
EXPOSE ${PROXY_TCP_PORT}/tcp
EXPOSE ${PORT}/udp

USER $GUNICORN_USER
WORKDIR $APP_PATH
ENTRYPOINT sh $APP_PATH/entrypoint.sh
