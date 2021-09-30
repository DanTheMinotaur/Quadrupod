from quadrupod.bot import move_servo, Servo
import uasyncio


def set_all_servos(degrees):
    async def func():
        for i in range(0, 11):
            await Servo(i).move(degrees, wait=1)

    uasyncio.run(func())


def set_servos(degrees, *args):
    async def func():
        for i in args:
            await move_servo(i, degrees, wait=1)

    uasyncio.run(func())

