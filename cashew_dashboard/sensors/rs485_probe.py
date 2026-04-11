import serial
import struct

ser = serial.Serial('/dev/ttyUSB0', baudrate=4800, timeout=1)

MOISTURE_CMD = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x0B])
PH_CMD       = bytes([0x01, 0x03, 0x00, 0x06, 0x00, 0x01, 0x64, 0x0B])

def read_register(cmd):
    ser.write(cmd)
    response = ser.read(7)
    if len(response) == 7:
        return struct.unpack('>H', response[3:5])[0]
    return None

def get_moisture():
    raw = read_register(MOISTURE_CMD)
    return round(raw / 10.0, 1) if raw is not None else None

def get_ph():
    raw = read_register(PH_CMD)
    return round(raw / 100.0, 2) if raw is not None else None
