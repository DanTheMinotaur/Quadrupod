from quadrupod.bot import move_servo
import uasyncio


def set_all_servos(degrees):
    async def func():
        for i in range(0, 11):
            await move_servo(i, degrees, wait=1)

    uasyncio.run(func())


def set_servos(degrees, *args):
    async def func():
        for i in args:
            await move_servo(i, degrees, wait=1)

    uasyncio.run(func())


# def move_servo(index, degree, wait=None):
#     async def func():
#         await move_servo(index, degree, wait)
#
#     uasyncio.run(func())

# def run():
#     uasyncio.run(set_all_servos(90))