#!/bin/bash

#ffmpeg -pattern_type glob -i "resized/*.png" resized_movie.mpg

#ffmpeg -pattern_type glob -i "resized/*.png" resized_movie.mkv

#ffmpeg -pattern_type glob -i "resized/*.png" resized_movie.avi

ffmpeg -pattern_type glob -i "resized/*.png" -c:v libxvid resized_movie_xvid.avi

#ffmpeg -pattern_type glob -i "resized/*.png" -c:v libxvid -q:v 1 resized_movie_xvid_qv1.avi

ffmpeg -pattern_type glob -i "resized/*.png" -c:v libxvid -q:v 10 resized_movie_xvid_qv10.avi

