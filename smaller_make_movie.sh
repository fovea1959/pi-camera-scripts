#!/bin/bash

# used to be -c:v libxvid 

ffmpeg -y -pattern_type glob -i "resized/*.png" -c:v mpeg4 -vtag xvid -q:v 1 resized_movie_xvid_qv1_suse.avi 

#ffmpeg -y -pattern_type glob -i "resized/*.png" -c:v mpeg4 -vtag xvid -q:v 10 resized_movie_xvid_qv10_suse.avi 

#ffmpeg -y -r 5 -pattern_type glob -i "resized/*.png" -c:v mpeg4 -vtag xvid -q:v 10 resized_movie_xvid_qv10_slow_suse.avi 
