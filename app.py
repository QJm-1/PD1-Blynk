from flask import Flask, render_template, jsonify
import time

# Flask App Initialization
app = Flask(__name__)

# --- Technical Parameters (Constants from Literature/Standards) ---
[span_6](start_span)[span_7](start_span)TARGET_PH_MIN = 6.5  # Per PNS/BAFS 183:2020[span_6](end_span)[span_7](end_span)
TARGET_PH_MAX = 7.0
[span_8](start_span)[span_9](start_span)[span_10](start_span)TEMP_UPPER_BOUND = 180.0 # Safety limit for anacardic acid[span_8](end_span)[span_9](end_span)[span_10](end_span)
TEMP_LOWER_BOUND = 80.0  # Optimal pre-heat threshold
JAM_CURRENT_THRESHOLD = 5.0 # Amps (detected via ACS712)

def read_sensor_data():
    """
    Simulates the Data Acquisition Process.
    [span_11](start_span)[span_12](start_span)In a live system, this reads from I2C (ADS1115/MLX90614)[span_11](end_span)[span_12](end_span).
    """
    # Mock data representing a typical extraction state
    raw_ph = 4.8 
    [span_13](start_span)[span_14](start_span)raw_moisture = 11.5 # %[span_13](end_span)[span_14](end_span)
    [span_15](start_span)[span_16](start_span)raw_temp = 145.0 # Celsius[span_15](end_span)[span_16](end_span)
    raw_current = 2.1 # Amps
    
    return raw_ph, raw_moisture, raw_temp, raw_current

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    ph, moisture, temp, current = read_sensor_data()
    
    # 1. [span_17](start_span)[span_18](start_span)Thermal Governance Logic[span_17](end_span)[span_18](end_span)
    thermal_status = "Stable"
    if temp >= TEMP_UPPER_BOUND:
        thermal_status = "CRITICAL: Overheating"
    elif temp < TEMP_LOWER_BOUND:
        thermal_status = "Pre-heating"

    # 2. Anti-Jamming Logic
    system_alert = "Normal"
    if current > JAM_CURRENT_THRESHOLD:
        system_alert = "MECHANICAL JAM DETECTED"

    # 3. [span_19](start_span)[span_20](start_span)[span_21](start_span)Dosing Requirement[span_19](end_span)[span_20](end_span)[span_21](end_span)
    lime_needed = 0
    if ph < TARGET_PH_MIN:
        # [span_22](start_span)[span_23](start_span)Simplified Stoichiometric Logic[span_22](end_span)[span_23](end_span)
        lime_needed = round((TARGET_PH_MAX - ph) * 50, 2) 

    return jsonify({
        "ph": ph,
        "moisture": f"{moisture}%",
        "temp": f"{temp}°C",
        "status": thermal_status,
        "alert": system_alert,
        "dosage": f"{lime_needed}g"
    })

if __name__ == '__main__':
    # [span_24](start_span)[span_25](start_span)host='0.0.0.0' allows access from mobile devices on the same network[span_24](end_span)[span_25](end_span)
    app.run(host='0.0.0.0', port=5000, debug=True)