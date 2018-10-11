#!/bin/bash

rm tmp.smaller.*.sh

SCRIPT=`mktemp -p . tmp.smaller.XXXXXXXX.sh`
./process_frames.py --input-directory ~/3620-pi-camera-1/timelapse/01 --resize resized --filter-file filter --script $SCRIPT --timestamp
rv=$?

if [[ $rv -eq 0 ]]; then
 parallel --eta < $SCRIPT
 rv=$?
fi
