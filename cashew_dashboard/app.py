from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

# --- Engineering Standards & Operating Bounds ---
# Establishing upper and lower bounds for process stability
[span_3](start_span)[span_4](start_span)TEMP_MAX = 180.0    # Limit to prevent degradation of anacardic acid[span_3](end_span)[span_4](end_span)
[span_5](start_span)TEMP_MIN = 80.0     # Required pre-heat threshold for extraction[span_5](end_span)
[span_6](start_span)[span_7](start_span)PH_TARGET_MIN = 6.5 # Per PNS/BAFS 183:2020 organic standards[span_6](end_span)[span_7](end_span)
PH_TARGET_MAX = 7.0
[span_8](start_span)[span_9](start_span)MOISTURE_TARGET_MIN = 40.0 # Target for stable bio-fertilizer[span_8](end_span)[span_9](end_span)
MOISTURE_TARGET_MAX = 50.0
JAM_THRESHOLD_AMPS = 5.5   # Current spike detection for anti-jamming

def get_realtime_sensors():
    """
    [span_10](start_span)[span_11](start_span)Simulated Sensor Acquisition Process[span_10](end_span)[span_11](end_span)
    Reads dual temperatures (MLX90614) and RS485 probe data.
    """
    return {
        [span_12](start_span)"ph": 4.8,          # Raw acidic state[span_12](end_span)
        [span_13](start_span)"moisture": 42.5,   # Within 40-50% target[span_13](end_span)
        [span_14](start_span)"temp": 145.0,      # Monitored near extrusion nozzle[span_14](end_span)
        [span_15](start_span)"current": 2.1      # Motor load monitoring[span_15](end_span)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/telemetry')
def telemetry():
    data = get_realtime_sensors()
    
    # --- Control Logic & Decision Making ---
    
    # 1. [span_16](start_span)[span_17](start_span)Thermal Governance (PWM Throttling)[span_16](end_span)[span_17](end_span)
    thermal_status = "Optimal"
    if data['temp'] >= TEMP_MAX:
        thermal_status = "CRITICAL: Throttling Motor"
    elif data['temp'] < TEMP_MIN:
        thermal_status = "Pre-heating"

    # 2. [span_18](start_span)[span_19](start_span)Anti-Jamming Logic[span_18](end_span)[span_19](end_span)
    jam_alert = False
    if data['current'] > JAM_THRESHOLD_AMPS:
        jam_alert = True # Logic to trigger reverse-and-clear routine

    # 3. [span_20](start_span)[span_21](start_span)Stoichiometric Dosing[span_20](end_span)[span_21](end_span)
    # Logic to calculate CaCO3 dosage for neutralization
    lime_dosage_g = 0
    if data['ph'] < PH_TARGET_MIN:
        lime_dosage_g = round((PH_TARGET_MAX - data['ph']) * 45.5, 2)

    return jsonify({
        "ph": data['ph'],
        "moisture": f"{data['moisture']}%",
        "temp": f"{data['temp']}°C",
        "status": thermal_status,
        "jam": jam_alert,
        "dosage": f"{lime_dosage_g}g"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
