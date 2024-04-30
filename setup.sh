#!/bin/bash

sudo rm -rf *
python3 -m venv vatsal
cd vatsal
source bin/activate
git clone https://github.com/udaysk3/Vatsal_Order_Mgmt.git
cd Vatsal_Order_Mgmt
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
kill -9 $(lsof -i:8000 -t) 2> /dev/null
gunicorn --bind 0.0.0.0:8000 ordermgmt.wsgi:application
