#!/bin/bash

python3 ./app.py &
PYPID=$!
java UdpClient &
JPID=$!
echo "$PYPID  $JPID" >> temp.txt

#skripta koja pokreće server na računalu
