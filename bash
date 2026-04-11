sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv -y

python3 -m venv venv
source venv/bin/activate

pip install flask flask-socketiosmbus2 RPi.GPIO pyserial adafruit-circuitpython-mlx90614 gpiozero
