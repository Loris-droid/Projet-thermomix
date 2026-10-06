import network
import time
import ubinascii
from machine import Pin, ADC

try:
    import usocket as socket
except:
    import socket


# LED et bouton
led = Pin(2, Pin.OUT)
button = Pin(35, Pin.IN, Pin.PULL_UP)
# LED éteinte au démarrage
led.value(0)


# On ouvre la page HTML
with open("index.html", "r") as file:
    html = file.read()


# Connexion Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():

    print("Connexion au point d'accès...")

    wlan.connect("WIFI_SI1", "wifisi01")

    while not wlan.isconnected():

        print("Connexion en cours...")
        time.sleep(0.5)


print("Station connectée au point d'accès")
print("Le serveur écoute à l'adresse IP =", wlan.ifconfig()[0])


# Création du serveur
s = socket.socket()

ai = socket.getaddrinfo("0.0.0.0", 80)
addr = ai[0][-1]

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(addr)
s.listen(5)


while True:
    if button.value() == 1:

        pin12.value(1)

    else:

        pin12.value(0)

    s.settimeout(0.1)

    try:    
        # On attend une demande du navigateur
        res = s.accept()

        client_s = res[0]
        client_addr = res[1]

        requete = client_s.recv(4096)

        print("Requête reçue =", requete)


        # Si le navigateur demande d'allumer la LED
        if b"GET /led/on" in requete:

            led.value(1)

            print("LED allumée")


        # Si le navigateur demande d'éteindre la LED
        elif b"GET /led/off" in requete:

            led.value(0)

            print("LED éteinte")


    # Réponse du serveur
    client_s.send(b"HTTP/1.1 200 OK\r\n")
    client_s.send(b"Content-Type: text/html\r\n")
    client_s.send(b"Connection: close\r\n")
    client_s.send(b"\r\n")

    client_s.send(html.encode())

    client_s.close()