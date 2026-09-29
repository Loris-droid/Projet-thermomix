from machine import *
from time import sleep

button = Pin(35, Pin.IN, Pin.PULL_UP)
pin12 = Pin(12, Pin.OUT)
pin13 = Pin(13, Pin.OUT)
pin14 = Pin(14, Pin.OUT)
pin12.value(0)
pin13.value(0)
pin14.value(0)

while True:
    if button.value() == 1 :
        pin12.value(1)
    else:
        pin12.value(0)