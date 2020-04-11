#!/bin/bash
web_func() {
	while true; do wget -q -O- http://master.cwalops.ca:32008/generateLoad > /dev/null ; sleep $[ ( $RANDOM % 4 )  + 1 ]s; done
	}

for i in $(seq 1 $1); 
do
	web_func &
done
wait
