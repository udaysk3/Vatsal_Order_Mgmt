#!/bin/bash

sudo rm -rf *
git clone https://github.com/udaysk3/Vatsal_Order_Mgmt.git
cd Vatsal_Order_Mgmt
kill -9 $(lsof -i:8000 -t) 2> /dev/null
pip install -r requirements.txt --break-system-packages
sudo cp /tmp/.env /Vatsal_Order_Mgmt/.env
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn --bind 0.0.0.0:8000 -w 4 --timeout 600 ordermgmt.wsgi:application