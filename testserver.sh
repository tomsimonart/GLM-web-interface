#!/bin/bash
source launch.sh
./lmpm_server.py -vv&
sleep 1.5
flask run
