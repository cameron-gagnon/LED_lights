#!/bin/sh

# find the server that is running and kill the process
ps -U root u | grep main.py | tee /dev/tty | sudo kill $(awk '{print $2}')

# re-run the server
echo "Running main server...\n"
PYTHONUNBUFFERED=1 nohup sudo ./main.py &
