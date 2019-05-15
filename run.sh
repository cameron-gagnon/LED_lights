#!/bin/sh

# find the server that is running and kill the process
ps -U root u | grep main.py | tee /dev/tty | sudo kill $(awk '{print $2}')

# restart the dash_button listener
# since pushd isn't supported in sh
home_dir=$(pwd)
#cd ../dash_button
#./run.sh

#cd ../alexa_lumen
#./run.sh

cd ../chatbot
./run.sh

cd ../botify
./run.sh

cd "$home_dir"

# re-run the server
echo "Running main server...\n"
nohup sudo ./main.py &
