#!/bin/bash
#rsync -av pi@3620-pi-camera-1.local:/var/log/LOCAL\* /home/wegscd/3620-pi-camera-1/


# first matching include or exclude is the one that takes effect
rsync -av --progress \
	--include "*-??00*" \
	--exclude "*" \
	-e "ssh -T -c aes128-ctr -o Compression=no -x" \
	wegscd@synology1.local:/volume1/homes/wegscd/timelapse_01/ \
	$HOME/3620-pi-camera-1/timelapse/01/ 
rv=$?

if [ $rv -eq 0 ] ; then
  rsync -av --progress \
	-e "ssh -T -c aes128-ctr -o Compression=no -x" \
	wegscd@synology1.local:/volume1/homes/wegscd/timelapse_01/ \
	$HOME/3620-pi-camera-1/timelapse/01/ 
  rv=$?
fi

echo status $rv

exit $rv

