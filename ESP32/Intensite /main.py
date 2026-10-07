from machine import ADC, Pin, PWM
from time import sleep

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)


led = PWM(Pin(14), freq=1000)

while True:
    valeur = pot.read()          
    intensite = valeur / 4095
    voltage = valeur * 3.3 / 4095
    led.duty(int(intensite * 1023))
    print("Pot:", "{:.2f} V".format(voltage),
          "Intensité:", "{:.2f}".format(intensite))
    sleep(0.05)
