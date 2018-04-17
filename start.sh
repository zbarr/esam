#!/bin/bash
cd /home/zbarr/dashboard
source /home/zbarr/dashboard/python_virtualenv/bin/activate
python salt_api.py
deactivate
