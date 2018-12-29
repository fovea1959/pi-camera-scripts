#!/bin/bash

rsync -av pi@3620-pi-camera-1.local:/var/log/LOCAL\* $HOME/3620-pi-camera-1/
rv=$?


if [ $rv -eq 0 ] ; then
  rsync -av --progress \
	--include "*-??00*" \
	--exclude "*" \
	-e "ssh -T -c aes128-ctr -o Compression=no -x" \
	pi@3620-pi-camera-1.local:/home/pi/timelapse/01/ \
	$HOME/3620-pi-camera-1/timelapse/01/
  rv=$?
fi

if [ $rv -eq 0 ] ; then
  rsync -av --progress \
	-e "ssh -T -c aes128-ctr -o Compression=no -x" \
	pi@3620-pi-camera-1.local:/home/pi/timelapse/01/ \
	$HOME/3620-pi-camera-1/timelapse/01/
  rv=$?
fi

echo status $rv

exit $rv
