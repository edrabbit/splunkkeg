#!/usr/bin/env python

import datetime
import serial
import urllib2
import json

# Serial port connection
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)

#print ser

pulses = 0
liters = 0
total_pulses = 0
keg_name = 'keg1'
of = open(keg_name+'.log', "a+",0)


while True:
# Read line received
    line = ser.readline().strip()
    #	if line:
    #		print line
    # Remove possible garbage lines
    if line.startswith('pulses'):
        piece = line.split(':')
        if 2==len(piece):
            pulses = int(piece[1].strip())
            #                print ("Pulses:",  pulses)
            total_pulses = total_pulses + pulses
            liters = float(total_pulses)/5600
            #                print ("Liters:", liters)
            data = {"timestamp":datetime.datetime.utcnow().isoformat(),
                    "keg":keg_name,
                    "total_pulses":total_pulses,
                    "pulses":pulses,
                    "consumption":round(liters, 3)}
            print data
            of.write(str(data)+'\n')