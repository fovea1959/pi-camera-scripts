#!/bin/bash

friday=`date -d 'last Friday' +%Y%m%d`
start=`dateutils.dadd -f "%Y%m%d" -i "%Y%m%d" $friday -4d`
echo friday was $friday, so doing since $start
rm weekly/*

if true; then
 rm tmp.weekly.*.sh
 SCRIPT=`mktemp -p . tmp.weekly.XXXXXXXX.sh`

 ./process_frames.py --input-directory ~/3620-pi-camera-1/timelapse/01 --resize weekly/ --filter-file filter --script $SCRIPT --start $start --end $friday
 rv=$?

 if [[ $rv -eq 0 ]]; then
  parallel --eta < $SCRIPT
  rv=$?
 fi
fi
