#!/bin/bash

while true
do
	nc -l 9000 | ./conf.sh
done
