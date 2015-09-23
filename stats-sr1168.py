#!/usr/bin/env python

import serial
from pprint import pprint

from statsd import StatsClient
statsd = StatsClient(host='stats',
                     port=8125,
                     prefix='sr1168c')

def CtoF (C):
  F = (C * 9/5) + 32
  return F

def stats_write ( arr ):
    print ' mark ===='
    for key,val in arr.iteritems():
        print key + ': ' + str(val)
        statsd.gauge(key, val)

ser = serial.Serial('/dev/ttyUSB-sr1168', 4800)

#send request
ser.write("\x01\x03\x00\x00\x00\x10\x14\x00")

# read 37 byte response
raw = ser.read(37)
data = raw[3:37]

#print data.encode('hex')

values = {}

values['t0'] = CtoF(ord(data[0])-10)
values['t1'] = CtoF(ord(data[1])-10)
values['t2'] = CtoF(ord(data[2]))
values['t3'] = CtoF(ord(data[3]))

values["pumptime"]   = (256 * ord(data[10]) + ord(data[11]))
values["e_kw"] 	     = (256 * ord(data[12]) + ord(data[13]))
values["e_accum_kw"] = (256 * ord(data[14]) + ord(data[15]))
values["e_accum_mw"] = (256 * ord(data[16]) + ord(data[17]))

byte = ord(data[20])
values['pump'] = byte & 0x01

stats_write(values)

