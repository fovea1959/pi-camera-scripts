#!/bin/bash -v
logger -p LOCAL7.info "dumping pijuice status"
/usr/local/bin/pijuice_util.py --get-alarm | logger -p LOCAL7.info
logger -p LOCAL7.info "running shutdown --poweroff command"
/sbin/shutdown --poweroff now | logger -P LOCAL7.info
rc=$?
logger -p LOCAL7.info "shutdown --poweroff command status $rc"
