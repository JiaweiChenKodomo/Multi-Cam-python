#!/bin/sh
echo "Run server!"
sleep 5
cd /home/peer/Desktop/MultiCamCui

python server3.py 2>/tmp/server.err >/tmp/server.log
