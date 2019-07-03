#!/usr/bin/env bash
python3 /home/pi/smarthome/control/control.py &
python3 /home/pi/smarthome/api_server.py &
python3 /home/pi/smarthome/web_ui/manage.py runserver 0.0.0.0:8088
