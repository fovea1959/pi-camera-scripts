#!/bin/bash
#rsync -av pi@3620-pi-camera-1.local:/var/log/LOCAL\* /home/wegscd/3620-pi-camera-1/
rsync -av --progress \
	$HOME/3620-pi-camera-1/scripts/*.avi \
	wegscd@synology1.local:/volume1/homes/wegscd/timelapse_movies/
