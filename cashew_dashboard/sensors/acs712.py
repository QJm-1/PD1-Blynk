import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel=0):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

def get_current_amps():
    raw = read_adc(0)
    voltage = (raw / 1023.0) * 5.0
    current = (voltage - 2.5) / 0.185  # ACS712-5A sensitivity
    return round(abs(current), 2)
