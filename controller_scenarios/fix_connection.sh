#!/bin/sh
echo "fix wifi"
pkill -f wpas
killall wpa_supplicant
sudo /usr/local/bin/start80211acStation.sh 
echo "wifi fixed"
