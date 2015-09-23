#!/usr/bin/env python

#!!!!!!!!!!!!!!!!!!! this is a work in progress - this script is broken.  Use the "stats" script.

import serial
from pprint import pprint

def CtoF (C):
  F = (C * 9/5) + 32
  return F

ser = serial.Serial('/dev/ttyUSB-sr1168', 4800)

#send request
ser.write("\x01\x03\x00\x00\x00\x10\x14\x00")

# read 37 byte response
raw = ser.read(37)
data = raw[3:37]

print data.encode('hex')

values = {}
sets = {}
status = {}

values['T0'] = CtoF(ord(data[0])-10)
values['T1'] = CtoF(ord(data[1])-10)
values['T2'] = CtoF(ord(data[2]))
values['T3'] = CtoF(ord(data[3]))
#values['T4'] = CtoF(ord(data[4]))
#values['T5'] = CtoF(ord(data[5]))
#values['T6'] = CtoF(ord(data[6]))

values["pumptime"]   = (256 * ord(data[10]) + ord(data[11]))
values["E_KW"] 	     = (256 * ord(data[12]) + ord(data[13]))
values["E_accum_KW"] = (256 * ord(data[14]) + ord(data[15]))
values["E_accum_MW"] = (256 * ord(data[16]) + ord(data[17]))

values['pump1perc'] = CtoF(ord(data[18]))
values['pump2perc'] = CtoF(ord(data[19]))

byte = ord(data[20])
values['P1'] = byte & 0x01
values['P2'] = byte & 0x02
values['P3'] = byte & 0x04
values['P4'] = byte & 0x08
values['H1'] = byte & 0x10

byte = ord(data[29])
values['R1'] = byte & 0x01
values['R2'] = byte & 0x02
values['R3'] = byte & 0x04
values['R1_DSP'] = byte & 0x08
values['R2_DSP'] = byte & 0x10

byte = ord(data[21])
#print bin(byte)
sets['Emergency Closing: Collector'] = byte & 0x01
sets['Low Temp Protection: Collector'] = byte & 0x02
sets['Anti-Frost Protection: Collector'] = byte & 0x04
sets['Re-Cooling: Colector'] = byte & 0x08
sets['High Temperature Protection: Tank'] = byte & 0x10
sets['Emergency Closing: Tank'] = byte & 0x12
sets['Dry Heat Protection'] = byte & 0x14


byte = ord(data[26])
#print byte
status['0Hot Water Pipe Circuit']   = byte & 0x01
status['1Setting Fahrenheit']       = byte & 0x02 
status['2Thermal Energy Measuring'] = byte & 0x04 
status['43Anti-Legionaires']        = byte & 0x08
status['5Bypass']                   = byte & 0x16
status['6Holiday']                  = byte & 0x32
status['7Manual Heating']           = byte & 0x64
status['8System Operation']         = byte & 0x128

for i in range(20,34):
  print str(i) + ": " + str(ord(data[i]))

pprint(values)
#pprint(sets)
#pprint(status)

