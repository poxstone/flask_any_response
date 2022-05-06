FROM alpine:latest
#FROM ubuntu:20.04

ENV APP_PORT=8080
ENV UDP_PORT=5005
ENV GUNICORN_MODULE='application'
ENV GUNICORN_CALLABLE='app'
ENV GUNICORN_USER='root'
ENV APP_PATH='/app'
ENV WORKERS='3' 
ENV TIMEOUT='120'
ENV INIT_APP_TIME='0'
ENV VERSION_DEP='vp.0.0.1b'
ENV UDP_PORT='5005'


RUN apk add --no-cache python3 \
    && apk add nmap mysql-client redis lsblk curl tcpdump tar tmux bind-tools stress-ng \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip gunicorn 
#    && adduser -D -h $APP_PATH $GUNICORN_USER

COPY ./ $APP_PATH

RUN pip3 install -r $APP_PATH/requirements.txt --upgrade

EXPOSE $APP_PORT
EXPOSE ${APP_PORT}/udp

USER $GUNICORN_USER
WORKDIR $APP_PATH
ENTRYPOINT sh $APP_PATH/entrypoint.sh
