#!/bin/bash
rsync -av pi@3620-pi-camera-1.local:/home/pi/timelapse/01/ /home/wegscd/3620-pi-camera-1/timelapse/01/
rsync -av pi@3620-pi-camera-1.local:/var/log/LOCAL\* /home/wegscd/3620-pi-camera-1/
