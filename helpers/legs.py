from quadrupod.bot import Leg
from quadrupod.utils import load_config
# from uasyncio import run, gather
import uasyncio

CONFIG = load_config('../config.json')


def create_legs(config):
    legs = []
    for ref, pos in config["legs"].items():
        legs.append(Leg(pos["u"], pos["m"], pos["l"], ref))
    return legs


LEGS = create_legs(CONFIG)


def get_leg(ref):
    for leg in LEGS:
        if leg.ref == ref:
            return leg


def defaults():
    async def func():
        moves = []
        for leg in LEGS:
            moves.append(leg.move_to_origin())
        await uasyncio.gather(*moves)
    uasyncio.run(func())


def test_all():
    async def func():
        await uasyncio.gather(*[leg.upper.move_to_default() for leg in LEGS])
        for leg in LEGS:
            await leg.move()


def stand():
    async def func():
        await uasyncio.gather(*[leg.lower.move_to_default() for leg in LEGS])
        mid_moves = []
        up_moves = []
        for leg in LEGS:
            mid_moves.append(leg.middle.move(leg.middle.percentage_to_degrees(0.5), 1.5))
            up_moves.append(leg.upper.move(leg.upper.percentage_to_degrees(0.2), 1.5))

        await uasyncio.gather(*up_moves)
        await uasyncio.gather(*mid_moves)
        # await uasyncio.sleep(1.5)

    uasyncio.run(func())
