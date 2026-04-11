import RPi.GPIO as GPIO
import time

STEP_PIN = 20
DIR_PIN  = 21
EN_PIN   = 16
STEPS_PER_ROTATION = 200

GPIO.setmode(GPIO.BCM)
for pin in [STEP_PIN, DIR_PIN, EN_PIN]:
    GPIO.setup(pin, GPIO.OUT)
GPIO.output(EN_PIN, GPIO.LOW)  # enable driver

def rotate(rotations, direction=1, delay=0.005):
    GPIO.output(DIR_PIN, direction)
    steps = int(rotations * STEPS_PER_ROTATION)
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)

def dose_lime(grams, grams_per_rotation=2.3):
    rotations = grams / grams_per_rotation
    rotate(rotations)
