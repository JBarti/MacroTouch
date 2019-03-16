#!/bin/bash
python3 ./app.py &
PYPID=$!
java UdpClient &
JPID=$!
echo "$PYPID  $JPID" >> PID.txt

