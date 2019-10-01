#!/bin/bash

echo stop
sudo systemctl stop voltlog.service

sleep 2

echo start
sudo systemctl start voltlog.service

echo 
echo done
echo 


echo systemctl status voltlog.service