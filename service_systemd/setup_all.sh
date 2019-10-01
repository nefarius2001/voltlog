#!/bin/bash


echo copy services and reload
cd ~/code/raspi-monitoring/service_systemd
sudo chmod 644 ./*.service
sudo cp        ./*.service /lib/systemd/system/
sudo systemctl daemon-reload

#echo #manual start/stop:
#echo sudo systemctl start logEnvironment_Sensors.service
#echo sudo systemctl start soundsocket.service
#echo sudo systemctl start websockets_sensordb.service
#
#echo #start service on every reboot:
#sudo systemctl enable logEnvironment_Sensors.service
#sudo systemctl enable soundsocket.service
#sudo systemctl enable websockets_sensordb.service
#
#echo #read journal:
#echo journalctl -f -u logEnvironment_Sensors.service
#echo journalctl -f -u soundsocket.service
#echo journalctl -f -u websockets_sensordb.service