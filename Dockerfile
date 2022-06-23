FROM alpine:latest
#FROM ubuntu:20.04

ENV APP_PORT=8080
ENV UDP_PORT=5005
ENV GUNICORN_MODULE='application'
ENV GUNICORN_CALLABLE='app'
ENV GUNICORN_USER='root'
ENV APP_PATH='/app'
ENV WORKERS='1'
ENV TIMEOUT='120'
ENV INIT_APP_TIME='0'
ENV VERSION_DEP='vp.0.0.2dock'
ENV UDP_PORT='5005'
# for gcp Profiler
#ENV GOOGLE_CLOUD_PROJECT=''


RUN apk add --no-cache python3 ca-certificates\
    && apk add nmap mysql-client redis lsblk curl tcpdump tar tmux bind-tools stress-ng \
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
    ln -s /opt/mssql-tools/bin/sqlcmd /usr/bin/sqlcmd && ln -s /opt/mssql-tools/bin/bcp /usr/bin/bcp

COPY ./ $APP_PATH

RUN pip3 install -r $APP_PATH/requirements.txt --upgrade

EXPOSE $APP_PORT
EXPOSE ${APP_PORT}/udp

USER $GUNICORN_USER
WORKDIR $APP_PATH
ENTRYPOINT sh $APP_PATH/entrypoint.sh
