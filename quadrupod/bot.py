from quadrupod import pca9685
from machine import Pin, SoftI2C
import uasyncio


class Servo:
    SERVOS = pca9685.Servos(SoftI2C(scl=Pin(5), sda=Pin(4)))
    WAIT_TIME = 1.5

    def __init__(self, index, origin_position=None):
        self.index = index
        self.__origin = origin_position
        self.__position = None

    @property
    def origin(self):
        return self.__origin

    @property
    def position(self):
        return self.__position

    async def move(self, degrees, wait=None):
        print(f"Index: {self.index} to {degrees} degrees")
        Servo.SERVOS.position(self.index, degrees)
        if wait:
            await uasyncio.sleep(wait)
        self.__position = degrees
        Servo.SERVOS.release(self.index)

    async def ensure_position(self):
        await self.move(self.__position, Servo.WAIT_TIME)

    async def move_to_default(self):
        await self.move(self.__origin, Servo.WAIT_TIME)

    def percentage_to_degrees(self, percentage_float=0.1):
        degree = float(percentage_float) * 180
        return int(abs(self.origin - degree))


class Leg:
    def __init__(self, u_idx, m_idx, l_idx, ref=None):
        self.__ref = ref
        origin = self.get_origin()
        self.upper = Servo(u_idx, origin)
        self.middle = Servo(m_idx, origin)
        self.lower = Servo(l_idx, 90)

    @property
    def servos(self):
        return self.upper, self.middle, self.lower

    @property
    def ref(self):
        return self.__ref

    async def move(self, upper_pos=None, middle_pos=None, lower_pos=None, wait=None):
        await uasyncio.gather(
            self.upper.move(upper_pos, wait),
            self.middle.move(middle_pos, wait),
            self.lower.move(lower_pos, wait)
        )

    def get_origin(self):
        return 180 if self.__ref in ['lb', 'rf'] else 0

    async def move_to_origin(self):
        await uasyncio.gather(*[s.move_to_default() for s in self.servos])


# Static Movement
class Quadruped:
    def __init__(self, config):
        self.__lf = None
        self.__lb = None
        self.__rf = None
        self.__rb = None
        for ref, pos in config["legs"].items():
            setattr(self, f"__{ref}", Leg(pos["u"], pos["m"], pos["l"], ref))

    @property
    def legs(self):
        return self.__lb, self.__lf, self.__rb, self.__rf

    def step(self):
        pass

    async def stand(self):
        await uasyncio.gather(*[leg.upper.move_to_default() for leg in self.legs])
        moves = []
        for leg in self.legs:
            move = 40 if leg.get_origin() > 0 else 140
            moves.append(leg.move(None, move))

    async def sit(self):
        await uasyncio.gather(*[leg.move_to_origin() for leg in self.legs])

