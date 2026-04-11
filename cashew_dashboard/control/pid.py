import time

class PIDController:
    def __init__(self, kp=1.2, ki=0.05, kd=0.4, setpoint=180):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self._integral = 0
        self._prev_error = 0
        self._last_time = time.time()

    def compute(self, current_temp):
        now = time.time()
        dt = now - self._last_time or 1e-6

        error = self.setpoint - current_temp
        self._integral += error * dt
        derivative = (error - self._prev_error) / dt

        output = (self.kp * error) + (self.ki * self._integral) + (self.kd * derivative)
        output = max(30, min(100, output))  # clamp PWM to 30–100%

        self._prev_error = error
        self._last_time = now
        return round(output, 1), round(error, 2)
