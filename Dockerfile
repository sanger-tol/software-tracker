FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq -y && \
    apt-get install -qq -y  python3-pip \
                            python3-flask \
                            gunicorn3 \
                            cifs-utils && \
    apt -y autoremove

ENV APP_USER="tracker" \
    APP_UID="1000" \
    APP_GROUP="tracker" \
    APP_GID="1000"

RUN set -ex; \
    groupadd -r --gid "$APP_GID" "$APP_GROUP"; \
    useradd -rm --uid "$APP_UID" --gid "$APP_GID" -d /home/"$APP_USER" "$APP_USER"

USER $APP_USER

RUN python3 -m pip install --user pipenv flask mysql-connector datetime
ENV PATH=/home/$APP_USER/.local/bin:$PATH

ARG APP_DIR=/home/$APP_USER/application
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

COPY html/ ${APP_DIR}/html
COPY api.py ${APP_DIR}
COPY start_production_server.sh ${APP_DIR}

CMD ./start_production_server.sh


