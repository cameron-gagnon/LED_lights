#!/bin/sh

PROGRAM_NAME="./pixelated.py"
# find the server that is running and kill the process
#ps -U root u | grep main.py | tee /dev/tty | sudo kill $(awk '{print $2}')
sudo pkill -f $PROGRAM_NAME

# re-run the server
echo "Running main server...\n"
PYTHONUNBUFFERED=1 nohup sudo $PROGRAM_NAME &
