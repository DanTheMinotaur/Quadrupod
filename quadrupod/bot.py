from quadrupod import pca9685
from machine import I2C, Pin, SoftI2C
import uasyncio


class Servo:
    SERVOS = pca9685.Servos(I2C(scl=Pin(5), sda=Pin(4)))
    WAIT_TIME = 1.5

    def __init__(self, index, default_position=None):
        self.index = index
        self.default_position = default_position
        self.position = None

    async def move(self, degrees, wait=None):
        print(f"Index: {self.index} to {degrees} degrees")
        Servo.SERVOS.position(self.index, degrees)
        if wait:
            await uasyncio.sleep(wait)
        self.position = degrees
        Servo.SERVOS.release(self.index)

    async def ensure_position(self):
        await self.move(self.position, Servo.WAIT_TIME)

    async def move_to_default(self):
        await self.move(self.default_position, Servo.WAIT_TIME)


class Leg:
    def __init__(self, u_idx, m_idx, l_idx, ref=None):
        self.position_ref = ref
        default_pos = self._default_pos()
        self.upper = Servo(u_idx, default_pos)
        self.middle = Servo(m_idx, default_pos)
        self.lower = Servo(l_idx, 90)

    @property
    def servos(self):
        return self.upper, self.middle, self.lower

    async def move(self, upper_pos=None, middle_pos=None, lower_pos=None, wait=None):
        await uasyncio.gather(
            self.upper.move(upper_pos, wait),
            self.middle.move(middle_pos, wait),
            self.lower.move(lower_pos, wait)
        )

    def _default_pos(self):
        d = 0
        if self.position_ref == 'lb' or self.position_ref == 'rf':
            d = 180
        return d

    async def move_to_default(self):
        await uasyncio.gather(*[s.move_to_default() for s in self.servos])

