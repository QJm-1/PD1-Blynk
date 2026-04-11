import board
import busio
import adafruit_mlx90614

i2c = busio.I2C(board.SCL, board.SDA)
mlx = adafruit_mlx90614.MLX90614(i2c)

def get_nozzle_temp():
    return round(mlx.object_temperature, 2)

def get_ambient_temp():
    return round(mlx.ambient_temperature, 2)
