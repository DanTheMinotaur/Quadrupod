from quadrupod import pca9685
from machine import I2C, Pin
import uasyncio

SERVOS = pca9685.Servos(I2C(scl=Pin(5), sda=Pin(4)))


async def move_servo(servo_index, degrees, wait=None):
    print(f"Index: {servo_index} to {degrees} degrees")
    SERVOS.position(servo_index, degrees)
    if wait:
        await uasyncio.sleep_ms(wait)
    SERVOS.release(servo_index)


class Leg:
    def __init__(self, u_idx, m_idx, l_idx):
        self.upper = u_idx
        self.middle = m_idx
        self.lower = l_idx

    async def move_to(self, upper_pos=None, middle_pos=None, lower_pos=None):
        await uasyncio.gather(
            self.upper.move(upper_pos),
            self.middle.move(middle_pos),
            self.lower.move(lower_pos)
        )
