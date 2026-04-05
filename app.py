from flask import Flask, render_template, jsonify
from hardware_interface import read_sensors
from predictor import get_required_dosage

app = Flask(__name__)

@app.route('/')
def index():
    # This loads the HTML file
    return render_template('index.html')

@app.route('/data')
def data():
    # This sends real-time sensor data as JSON
    ph, moisture, temp = read_sensors()
    dosage = get_required_dosage(ph, moisture, temp)
    
    return jsonify({
        'ph': round(ph, 2),
        'moisture': round(moisture, 1),
        'temp': round(temp, 1),
        'dosage': dosage
    })

if __name__ == '__main__':
    # '0.0.0.0' makes it accessible to other devices on the same WiFi
    app.run(host='0.0.0.0', port=5000, debug=True)
