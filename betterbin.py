#!/usr/bin/env python3
import serial

port = '/dev/ttyUSB0'
UV = '1'
INFRARED = '2'

if __name__ == "__main__":
    ser = serial.Serial(port, 9600, 1)
    ser.reset_input_buffer()

def readUV():
    ser.write((UV + '\n').encode('utf-8'))
    while not ser.in_waiting:
        pass
    return int.from_bytes(ser.read(), byteorder = 'big')
    
def readInfrared():
    ser.write((INFRARED + '\n').encode('utf-8'))
    while not ser.in_waiting:
        pass
    return int.from_bytes(ser.read(), byteorder = 'big')
