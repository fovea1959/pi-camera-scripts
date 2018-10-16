#!/bin/bash
rsync -av pi@3620-pi-camera-1.local:/var/log/LOCAL\* $HOME/3620-pi-camera-1/
rsync -av --progress pi@3620-pi-camera-1.local:/home/pi/timelapse/01/ $HOME/3620-pi-camera-1/timelapse/01/
