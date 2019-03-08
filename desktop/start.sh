#!/bin/bash
python3 ./app.py &
java UdpClient 
pkill python3
