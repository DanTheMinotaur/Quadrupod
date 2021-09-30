from quadrupod import pca9685
from machine import I2C, Pin
import uasyncio


class Servo:
    SERVOS = pca9685.Servos(I2C(scl=Pin(5), sda=Pin(4)))

    def __init__(self, idx):
        self.index = idx
        self.degrees = None

    async def move(self, degrees, wait=None):
        print(f"Index: {self.index} to {degrees} degrees")
        Servo.SERVOS.position(self.index, degrees)
        if wait:
            await uasyncio.sleep(wait)
        self.degrees = degrees
        Servo.SERVOS.release(self.index)

    async def ensure_position(self):
        Servo.SERVOS.position(self.index, self.degrees)
        await uasyncio.sleep(0.5)


class Leg:
    def __init__(self, u_idx, m_idx, l_idx, ref=None):
        self.upper = Servo(u_idx)
        self.middle = Servo(m_idx)
        self.lower = Servo(l_idx)
        self.ref = ref

    async def move(self, upper_pos=None, middle_pos=None, lower_pos=None, wait=None):
        await uasyncio.gather(
            self.upper.move(upper_pos),
            self.middle.move(middle_pos),
            self.lower.move(lower_pos)
        )



