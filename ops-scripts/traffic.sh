#!/bin/bash
web_func() {
	while true; do curl -s http://master.cwalops.ca:32008/productpage > /dev/null ; sleep $[ ( $RANDOM % 4 )  + 1 ]s; done
	}

for i in $(seq 1 $1); 
do
	web_func &
done
wait
