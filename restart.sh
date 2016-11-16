#!/bin/bash

# find the server that is running and kill the process
ps aux | grep 'run.py' | sudo kill $(awk '{print $2}')

# re-run the server
nohup sudo ./run.py &
