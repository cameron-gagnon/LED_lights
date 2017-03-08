#!/bin/sh

# find the server that is running and kill the process
ps aux | grep 'main.py' | sudo kill $(awk '{print $2}')


# restart the dash_button listener
# since pushd isn't supported in sh
home_dir=$(pwd)
cd ../dash_button
./run.sh

cd ../alexa_lumen
./run.sh

cd "$home_dir"

# re-run the server
nohup sudo ./main.py &
