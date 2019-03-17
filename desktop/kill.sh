#!/bin/bash

pids=`cat PID.txt`

echo "" > PID.txt

for word in $pids
do
    kill 9 $word
done

#skripta koja gasi server na računalu
