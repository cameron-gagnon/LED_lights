#!/bin/bash

if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo"
    echo "sudo $0 $*"
    exit 1
fi

service_name="pixelated"
filename="${service_name}.service"
username=$(logname)

echo "#!/bin/bash" > $filename
echo "[Unit]" >> $filename
echo "Description=LED strip controller for Stroop\'s room" >> $filename
echo "" >> $filename
echo "[Install]" >> $filename
echo "WantedBy=multi-user.target" >> $filename
echo "" >> $filename
echo "[Service]" >> $filename
echo "User=$username" >> $filename
echo "Type=forking" >> $filename
echo "WorkingDirectory=/home/$username/src/$service_name" >> $filename
echo "ExecStart=/home/$username/src/$service_name/run.sh" >> $filename
echo "Restart=always" >> $filename
echo "RestartSec=3" >> $filename

# since this script is run as root, need to re-own the output service file
# back to the user
chown $username:$username $filename

cp $filename /etc/systemd/system/$filename
