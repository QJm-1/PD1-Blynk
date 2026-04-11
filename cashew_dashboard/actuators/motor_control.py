import RPi.GPIO as GPIO

MOTOR_PWM_PIN = 18  # BCM numbering

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PWM_PIN, GPIO.OUT)
pwm = GPIO.PWM(MOTOR_PWM_PIN, 1000)  # 1kHz frequency
pwm.start(0)

def set_motor_speed(percent):
    percent = max(0, min(100, percent))
    pwm.ChangeDutyCycle(percent)

def stop_motor():
    pwm.ChangeDutyCycle(0)

def reverse_motor(duration=2):
    import time
    stop_motor()
    time.sleep(0.3)
    set_motor_speed(40)   # slow reverse
    time.sleep(duration)
    stop_motor()

def cleanup():
    pwm.stop()
    GPIO.cleanup()
