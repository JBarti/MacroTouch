#!/bin/bash

pids=`cat temp.txt`

echo "" > temp.txt

for word in $pids
do
    kill 9 $word
done

#skripta koja gasi server na računalu
