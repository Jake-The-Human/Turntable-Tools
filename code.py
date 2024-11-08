import time
import board
from modules.screen import Screen
from modules.mems_sensor import MemsSensor

i2c = board.STEMMA_I2C()

sensor = MemsSensor(i2c)
screen = Screen(board.I2C())

sensor.setOffset()

while True:
    screen.display(sensor.getAcceleration(), sensor.getGyro(), sensor.getRPM(), sensor.getDegrees())
    btn_a, btn_b, btn_c = screen.checkButtons()
    if btn_a:
        sensor.setOffset()
    time.sleep(0.5)
    
