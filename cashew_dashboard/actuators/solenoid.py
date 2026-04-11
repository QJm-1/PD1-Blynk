import RPi.GPIO as GPIO
import time

RELAY_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)  # relay off by default

def mist_on():
    GPIO.output(RELAY_PIN, GPIO.LOW)

def mist_off():
    GPIO.output(RELAY_PIN, GPIO.HIGH)

def mist_pulse(seconds=2):
    mist_on()
    time.sleep(seconds)
    mist_off()
