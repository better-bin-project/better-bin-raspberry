#!/usr/bin/env python3
import serial

PORT = '/dev/ttyUSB0'
UV = '1'
RGB = '2'

def readUV():
    ser.write((UV + '\n').encode('utf-8'))
    while not ser.in_waiting:
        pass
    return int.from_bytes(ser.read(), byteorder = 'big')
    
def readRGB():
    ser.write((RGB + '\n').encode('utf-8'))
    rgbData = {}
    for key in ['r', 'g', 'b', 'c']:
        while not ser.in_waiting:
            pass
        rgbData[key] = int.from_bytes(ser.read(), byteorder = 'big')
    return rgbData

if __name__ == "__main__":
    ser = serial.Serial(PORT, 9600)
    ser.reset_input_buffer()

    try:
        while True:
            print(readUV())
    except KeyboardInterrupt:
        ser.close()
