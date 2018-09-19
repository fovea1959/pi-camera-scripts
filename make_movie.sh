#!/bin/bash

./filter_symlinks.py --input-directory ~/3620-pi-camera-1/timelapse/01 --output o --filter-file filter
rv=$?

if [[ $rv -eq 0 ]]; then
 ffmpeg -pattern_type glob -i "o/*.jpg" movie.mpg
 rv=$?
fi

if [[ $rv -eq 0 ]]; then
 ffmpeg -pattern_type glob -i "o/*.jpg" movie.mkv
 rv=$?
fi
