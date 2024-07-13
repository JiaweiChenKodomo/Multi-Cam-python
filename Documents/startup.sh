#!/bin/sh
echo "Run server!"
sleep 5
# Change to the project directory.
cd /home/peer/Desktop/MultiCamCui

python server3.py 2>/tmp/server.err >/tmp/server.log
