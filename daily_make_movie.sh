#!/bin/bash -vx

function go() {
 T=`mktemp daily.$1.XXXXXX.txt`
 find $HOME/3620-pi-camera-1/scripts/resized/ -name "*$1*" -name "*.png" -printf "file '%H%P'\\n" | sort > $T

 ffmpeg -y -r 5 -safe 0 -f concat -i $T -c:v mpeg4 -vtag xvid -q:v 10 $1_suse.avi 

 #rm $T
}

go 20181001
go 20181002
go 20181003
go 20181004
go 20181005

go 20181008
go 20181009
go 20181010
go 20181011
go 20181012

go 20181015
go 20181016
go 20181017
go 20181018
go 20181019

go 20181022
go 20181023
go 20181024
go 20181025
go 20181026

go 20181029
go 20181030
go 20181031
