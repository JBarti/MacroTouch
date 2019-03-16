#!/bin/bash
python3 ./app.py &
PYPID=$!
echo $PYPID
java UdpClient 
kill 9 $PYPID
