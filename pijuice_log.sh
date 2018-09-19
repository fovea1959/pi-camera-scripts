#!/bin/bash

PIJUICE=/usr/local/bin/pijuice_util.py

(echo -n "input: " ; $PIJUICE --get-input ) | logger -p LOCAL7.INFO
(echo -n "battery: " ; $PIJUICE --get-battery ) | logger -p LOCAL7.INFO
(echo -n "disk: " ; ( df -h / | tail -n 1 )) | logger -p LOCAL7.info
