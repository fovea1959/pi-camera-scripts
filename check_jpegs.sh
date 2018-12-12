#!/bin/bash

find $HOME/3620-pi-camera-1/timelapse/01 -type f -name \*.jpg | sort | while read FILE; do
 if ! djpeg -fast -grayscale -onepass $FILE > /dev/null; then
  echo that bad file was $FILE
 fi
done
