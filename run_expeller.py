import time
import board
import busio
import adafruit_mlx90614
import RPi.GPIO as GPIO
import joblib
import warnings

# Suppress scikit-learn version warnings during live execution
warnings.filterwarnings("ignore", category=UserWarning)

# --- Hardware Configuration ---
RELAY_PIN = 4 # GPIO 4 (Pin 7 on the Pi)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW) # Fail-safe: Start with the machine OFF

# Setup I2C for the GY-906 Thermal Sensor
try:
    i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
    mlx = adafruit_mlx90614.MLX90614(i2c)
except Exception as e:
    print(f"[HARDWARE ERROR] Cannot connect to I2C sensor: {e}")
    GPIO.cleanup()
    exit()

# --- Load the AI Model ---
try:
    print("Loading Random Forest Model...")
    # This must be in the same folder as this script
    model = joblib.load('expeller_rf_model.pkl') 
    print("Model Loaded Successfully!")
except Exception as e:
    print(f"[SOFTWARE ERROR] Failed to load the .pkl model: {e}")
    GPIO.cleanup()
    exit()

print("========================================")
print("CNSL Expeller: Live Cyber-Physical Control")
print("Press Ctrl+C to Trigger Emergency Stop")
print("========================================")

try:
    while True:
        # 1. Read Live Sensors
        ambient_temp = mlx.ambient_temperature
        nozzle_temp = mlx.object_temperature
        
        # 2. Format data for the Random Forest
        # Must match the order trained: [Nozzle_Temp, Ambient_Temp]
        live_data = [[nozzle_temp, ambient_temp]]
        
        # 3. AI Inference
        # Returns an array, so we grab the first element [0]
        state = model.predict(live_data)[0] 
        
        # 4. Print Status to Terminal
        print(f"Nozzle: {nozzle_temp:.1f}°C | Ambient: {ambient_temp:.1f}°C | AI State Decision: {state}")
        
        # 5. Actuate the Hardware Logic Gates
        if state == 1:
            # State 1: Optimal Extraction Range -> Turn ON Relay
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            print("   -> SYSTEM RUNNING: Motors Active")
            
        elif state == 0:
            # State 0: Pre-heating / Too Cold -> Turn OFF Relay
            GPIO.output(RELAY_PIN, GPIO.LOW)
            print("   -> SYSTEM WAITING: Heating Block Active")
            
        elif state == 2:
            # State 2: Overheating -> Turn OFF Relay to prevent burning
            GPIO.output(RELAY_PIN, GPIO.LOW)
            print("   -> SYSTEM HALTED: Overheat Protection Engaged")
        
        # Delay to prevent flooding the CPU (1 Hz evaluation rate is perfect for thermal mass)
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[EMERGENCY STOP] Manual override initiated.")
finally:
    # --- Absolute Failsafe ---
    # If the script crashes or is stopped, ALWAYS kill the motor power.
    GPIO.output(RELAY_PIN, GPIO.LOW)
    GPIO.cleanup()
    print("Hardware Pins Reset. Machine safely powered down.")
