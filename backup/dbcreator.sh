#!/bin/bash

cd /home/zbarr/salt-app
: git pull
cd /home/zbarr/esam
source /home/zbarr/esam/python_virtualenv/bin/activate
python dbcreator.py
deactivate
