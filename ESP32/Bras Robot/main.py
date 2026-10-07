import network
import time
import ubinascii
from machine import Pin

try:
    import usocket as socket
except:
    import socket


# LED 
led = Pin(12, Pin.OUT)

# LED éteinte au démarrage
led.value(0)


# On ouvre la page HTML
with open("indx.html", "r") as file:
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
    s.settimeout(0.1)

    try:    
        # On attend une demande du navigateur
        res = s.accept()

        client_s = res[0]
        client_addr = res[1]

        requete = client_s.recv(4096)

        print("Requête reçue =", requete)

        if b"GET /led/on" in requete:

            led.value(1)

            print("LED allumée")


     
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
    except OSError:
        pass   