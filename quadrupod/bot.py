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


class Servo:
    def __init__(self, idx):
        self.index = idx

    async def move(self, degrees, wait=None):
        print(f"Index: {self.index} to {degrees} degrees")
        SERVOS.position(self.index, degrees)
        if wait:
            await uasyncio.sleep_ms(wait)
        SERVOS.release(self.index)


class Leg:
    def __init__(self, u_idx, m_idx, l_idx, ref=None):
        self.upper = Servo(u_idx)
        self.middle = Servo(m_idx)
        self.lower = Servo(l_idx)
        self.ref = ref

    async def move_to(self, upper_pos=None, middle_pos=None, lower_pos=None):
        await uasyncio.gather(
            self.upper.move(upper_pos),
            self.middle.move(middle_pos),
            self.lower.move(lower_pos)
        )



