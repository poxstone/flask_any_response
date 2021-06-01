FROM alpine:latest

ENV UDP_PORT=5005
ENV GUNICORN_USER='user_gun'
ENV APP_PATH='/app'
ENV VERSION_DEP='vp.0.0.1b'

RUN apk add --no-cache python3 \
    && python3 -m ensurepip \
    && adduser -D -h $APP_PATH $GUNICORN_USER

COPY ./ $APP_PATH

#RUN pip3 install -r $APP_PATH/requirements.txt --upgrade

EXPOSE ${UDP_PORT}/udp

USER $GUNICORN_USER
WORKDIR $APP_PATH
ENTRYPOINT sh $APP_PATH/entrypoint.sh
