#!/bin/bash
sudo apt-get update && \
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip python3-flask gunicorn3 cifs-utils && \
python3 -m pip install --user pipenv flask mysql-connector
export PATH=/home/ubuntu/.local/bin:$PATH
sudo apt -y autoremove
