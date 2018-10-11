#!/bin/bash

ffmpeg -y -pattern_type glob -i "weekly/*.png" -c:v libxvid -q:v 10 weekly_movie_xvid_qv10.avi

