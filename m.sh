#!/bin/bash

cd xx
for f in *; do
	n=`echo $f | perl -pe "s/^.*_//"`
	echo $f $n
	ln -s ../xx/$f ../s_xx/$n
done
