from flask import Flask, render_template
from flask_socketio import SocketIO
import threading, time, json

from sensors.mlx90614 import get_nozzle_temp
from sensors.rs485_probe import get_moisture, get_ph
from sensors.acs712 import get_current_amps
from actuators.motor_control import set_motor_speed, stop_motor, reverse_motor
from actuators.stepper import dose_lime
from actuators.solenoid import mist_pulse
from control.pid import PIDController
from control.fsm import ProcessFSM, State
from control.stoichiometry import calculate_lime_dose

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

fsm = ProcessFSM()
pid = PIDController(setpoint=180)
running = False
lime_total = 0.0

@app.route('/')
def index():
    return render_template('index.html')

def sensor_loop():
    global running, lime_total
    while True:
        if not running:
            time.sleep(0.5)
            continue

        temp     = get_nozzle_temp()
        moisture = get_moisture()
        ph       = get_ph()
        current  = get_current_amps()

        sensor_data = {
            'temp': temp,
            'moisture': moisture,
            'ph': ph,
            'compost_moisture': moisture if fsm.state == State.CONDITIONING else 0,
            'current': current
        }

        event = fsm.transition(sensor_data)
        pwm_output, pid_error = pid.compute(temp)

        if event == 'JAM_DETECTED':
            stop_motor()
            socketio.emit('alert', {'type': 'danger', 'msg': f'JAM detected! Current: {current}A. Reversing motor.'})
            reverse_motor(duration=2)
            set_motor_speed(pwm_output * 0.6)

        elif event == 'OVERHEAT_WARNING':
            socketio.emit('alert', {'type': 'warn', 'msg': f'High temp {temp}°C — PWM throttled to {pwm_output}%'})

        if fsm.state == State.EXTRACTING:
            set_motor_speed(pwm_output)

        if fsm.state == State.CONDITIONING:
            lime_needed = calculate_lime_dose(ph)
            if lime_needed > 0:
                dose_lime(lime_needed)
                lime_total += lime_needed
                mist_pulse(seconds=1.5)

        payload = {
            'fsm_state': fsm.state.name,
            'temp': temp,
            'moisture': moisture,
            'ph': ph,
            'current': current,
            'pwm': pwm_output,
            'pid_error': pid_error,
            'lime_total': round(lime_total, 1),
            'lime_dose': calculate_lime_dose(ph) if ph else 0
        }
        socketio.emit('sensor_data', payload)
        time.sleep(1)

@socketio.on('start_cycle')
def handle_start():
    global running, lime_total
    running = True
    lime_total = 0.0
    fsm.start()
    socketio.emit('alert', {'type': 'info', 'msg': 'Cycle started. Pre-heating...'})

@socketio.on('stop_cycle')
def handle_stop():
    global running
    running = False
    stop_motor()
    socketio.emit('alert', {'type': 'info', 'msg': 'Cycle stopped by user.'})

if __name__ == '__main__':
    thread = threading.Thread(target=sensor_loop, daemon=True)
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)



import sys

# Mock Pi-only libraries for Windows testing
if sys.platform == 'win32':
    from unittest.mock import MagicMock
    sys.modules['RPi']                    = MagicMock()
    sys.modules['RPi.GPIO']               = MagicMock()
    sys.modules['smbus2']                 = MagicMock()
    sys.modules['board']                  = MagicMock()
    sys.modules['busio']                  = MagicMock()
    sys.modules['adafruit_mlx90614']      = MagicMock()
    sys.modules['spidev']                 = MagicMock()
    sys.modules['serial']                 = MagicMock()

# Only AFTER the mocks, import everything else
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading, time

from sensors.mlx90614 import get_nozzle_temp
from sensors.rs485_probe import get_moisture, get_ph
from sensors.acs712 import get_current_amps
from actuators.motor_control import set_motor_speed, stop_motor, reverse_motor
from actuators.stepper import dose_lime
from actuators.solenoid import mist_pulse
from control.pid import PIDController
from control.fsm import ProcessFSM, State
from control.stoichiometry import calculate_lime_dose