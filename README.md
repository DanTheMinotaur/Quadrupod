# Quadrupod
A 3D printed quadruped built the ESP32 and PCA9685, code is written using Python. 

## Setup
Install [MicroPython](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) on the ESP32,

### Erase Flash Memory
```shell
sudo chmod 777 /dev/ttyUSB0
esptool.py --port /dev/ttyUSB0 erase_flash
```

### Install Firmware
```shell
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 ./firmware/esp32-20210902-v1.17.bin
```

## Run REPL
```shell
picocom /dev/ttyUSB0 -b 115200
```
Exit with Ctrl + AX

## Install Code

Install Ampy [More Info](https://core-electronics.com.au/tutorials/copy-files-to-micropython.html)

```shell
pip install adafruit-ampy
```

Test Ampy

```shell
ampy --port /dev/ttyUSB0  -b 115200 run ./helpers/blink_led.py
```

Ampy Commands

```shell
ampy -p /dev/ttyUSB0 put ./quadrupod/
ampy -p /dev/ttyUSB0 put ./helpers/
ampy -p /dev/ttyUSB0 ls 
```

# REPL commands

## Legs

```python
from helpers.legs import *
from uasyncio import run
lf, lb, rf, rb = get_leg("lf"), get_leg("lb"), get_leg("rf"), get_leg("rb")
run(lf.lower.move(90, 1))
```
