#!/usr/bin/env python

import serial
from influxdb import InfluxDBClient

def influx(measurement, item, value):
    json_body = [
        {
            "measurement": measurement,
            "tags": {
                "item": item 
            },
            "fields": {
                "value": float(value)
            }
        }
    ]

    client = InfluxDBClient('stats.311cub.net', 8086, 'root', 'root', 'sr1168')
    client.write_points(json_body)


def CtoF(C):
    F = (C * 9 / 5) + 32
    return F

ser = serial.Serial('/dev/ttyUSB-sr1168', 4800)

# send request
ser.write("\x01\x03\x00\x00\x00\x10\x14\x00")

# read 37 byte response
raw = ser.read(37)
data = raw[3:37]

# print data.encode('hex')

influx('temperature', 't0', CtoF(ord(data[0]) - 10))
influx('temperature', 't1', CtoF(ord(data[1]) - 10))
influx('temperature', 't2', CtoF(ord(data[2])))
influx('temperature', 't3', CtoF(ord(data[3])))

influx('time', 'pump', (256 * ord(data[10]) + ord(data[11])))
influx('power', 'e_kw', (256 * ord(data[12]) + ord(data[13])))
influx('power', 'e_accum_kw', (256 * ord(data[12]) + ord(data[15])))
influx('power', 'e_accum_mw', (256 * ord(data[12]) + ord(data[17])))

byte = ord(data[20])
influx('state', 'pump', byte & 0x01)
