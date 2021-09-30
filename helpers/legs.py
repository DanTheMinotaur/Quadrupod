from quadrupod.bot import Leg
from quadrupod.utils import load_config

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
