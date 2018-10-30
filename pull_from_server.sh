#!/bin/bash
#rsync -av pi@3620-pi-camera-1.local:/var/log/LOCAL\* /home/wegscd/3620-pi-camera-1/
rsync -av --progress \
	wegscd@synology1.local:/volume1/homes/wegscd/timelapse_01/ \
	$HOME/3620-pi-camera-1/timelapse/01/ 

