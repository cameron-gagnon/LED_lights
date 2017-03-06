#!/bin/bash

# find the server that is running and kill the process
ps aux | grep 'main.py' | sudo kill $(awk '{print $2}')


# restart the dash_button listener
#../dash_button/run.sh

# re-run the server
nohup sudo ./main.py &
