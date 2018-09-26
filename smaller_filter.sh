#!/bin/bash

./process_frames.py --input-directory ~/3620-pi-camera-1/timelapse/01 --resize resized --filter-file filter --script script.sh
rv=$?

if [[ $rv -eq 0 ]]; then
 parallel --eta < script.sh
 rv=$?
fi
