from machine import Pin
from time import sleep

INTERNAL_LED = Pin(2, Pin.OUT)

while True:
    for state in [0, 1]:
        INTERNAL_LED.value(state)
        sleep(0.2)
