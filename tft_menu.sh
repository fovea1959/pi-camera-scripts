#!/bin/bash

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

cd $SCRIPTPATH

errors=0

reset

while true; do

 cmd=`tft-menu.py fetchpush_menu.json 2> tft-menu.log`
 rv=$?
 if [ $rv -ne 0 ]; then
  ((errors++))
  break
 fi

 if [ "$cmd" = "exit" ]; then
  break
 fi

 $cmd

 echo touch screen to continue
 tft-dump-events.py -1
 rv=$?
 if [ $rv -ne 0 ]; then
  echo tft-dump-events got rc $rv
  break
 fi
 
done

if [ $errors -ne 0 ]; then
 echo $errors error\(s\)
 cat < tft-menu.log
 exit 1
fi
exit 0
