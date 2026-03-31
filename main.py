import time
import blynklib

# --- CONFIGURATION ---
# Replace this with the Auth Token from your Blynk Web Console
BLYNK_AUTH = 'YOUR_BLYNK_AUTH_TOKEN_HERE'

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# --- SYSTEM THRESHOLDS ---
MAX_TEMP_C = 180.0       # Threshold for anacardic acid degradation
JAM_CURRENT_A = 15.0     # Amperage spike indicating a mechanical jam (tune this)
TARGET_PH_MIN = 6.5      # Bio-fertilizer target pH
TARGET_PH_MAX = 7.0

def read_sensors():
    """
    TODO: Replace these hardcoded values with actual code to read from 
    your Raspberry Pi GPIO / I2C pins (MLX90614, pH probe, ACS712, etc.)
    """
    # Simulating data for initial testing
    return {
        "temp": 85.0,        
        "moisture": 45.0,    
        "ph": 4.8,           # Raw acidic cake
        "current": 5.2       # Normal operating current
    }

def process_alerts(data):
    """
    Evaluates sensor data against thresholds and sends alerts to the mobile app.
    Note: You must set up "Events" in the Blynk Web Console with these exact names.
    """
    # 1. Check for Mechanical Jams (Current Spike)
    if data["current"] >= JAM_CURRENT_A:
        print("ALERT: Mechanical Jam Detected!")
        blynk.log_event("mechanical_jam", f"Motor current spiked to {data['current']}A")
        # TODO: Add logic here to kill the motor or trigger reverse rotation
        
    # 2. Check for Thermal Runaway
    if data["temp"] >= MAX_TEMP_C:
        print("WARNING: Approaching Thermal Limit!")
        blynk.log_event("thermal_warning", f"Temperature reached {data['temp']}°C")
        # TODO: Add logic here to throttle PWM motor speed

    # 3. Check for Conditioning Completion
    if TARGET_PH_MIN <= data["ph"] <= TARGET_PH_MAX:
        print("STATUS: Conditioning Complete!")
        blynk.log_event("batch_complete", f"Target pH achieved: {data['ph']}")

def main():
    print("Connecting to IoT Dashboard...")
    
    while True:
        # Keep the connection to the Blynk Cloud alive
        blynk.run()
        
        # 1. Fetch data from your hardware
        sensor_data = read_sensors()
        
        # 2. Push metrics to Blynk Virtual Pins
        # Set up widgets in your mobile app assigned to these specific pins
        blynk.virtual_write(1, sensor_data["temp"])      # Datastream V1
        blynk.virtual_write(2, sensor_data["moisture"])  # Datastream V2
        blynk.virtual_write(3, sensor_data["ph"])        # Datastream V3
        blynk.virtual_write(4, sensor_data["current"])   # Datastream V4
        
        # 3. Run safety and completion checks
        process_alerts(sensor_data)
        
        # Delay to prevent spamming the cloud server (update every 2 seconds)
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSystem gracefully shut down.")
