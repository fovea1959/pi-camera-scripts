#!/usr/bin/env python
#
# This script is started at reboot by cron
# Since the start is very early in the boot sequence we wait for the i2c-1 device

import pijuice, time, os, syslog

syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_LOCAL7)

syslog.syslog('waiting for i2c-1')
while not os.path.exists('/dev/i2c-1'):
    time.sleep(0.1)

syslog.syslog('waiting for rtc')
while not os.path.exists('/dev/rtc'):
    time.sleep(0.1)

pj = pijuice.PiJuice(1, 0x14)

rtc = pj.rtcAlarm
ctr = rtc.GetControlStatus()
syslog.syslog(str(ctr))

syslog.syslog('disabling wakeup')
rtc.SetWakeupEnabled(False)

ctr = rtc.GetControlStatus()
syslog.syslog(str(ctr))

syslog.syslog('enabling wakeup')
rtc.SetWakeupEnabled(True)
syslog.syslog('wakeup enabled')

ctr = rtc.GetControlStatus()
syslog.syslog(str(ctr))
