#!/bin/bash

cd /home/qrcode_admin

source .venv/bin/activate

cd bin
python qrcode_val.py -d jettindersingh.com -p 80 &
