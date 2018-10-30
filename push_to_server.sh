#!/bin/bash
#rsync -av pi@3620-pi-camera-1.local:/var/log/LOCAL\* /home/wegscd/3620-pi-camera-1/
rsync -av --progress \
	$HOME/3620-pi-camera-1/timelapse/01/ \
	wegscd@synology1.local:/volume1/homes/wegscd/timelapse_01
