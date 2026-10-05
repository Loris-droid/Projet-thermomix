import network
import socket
import time
from machine import Pin
import ubinascii
import uhashlib

# Broches
button = Pin(35, Pin.IN, Pin.PULL_UP)
led = Pin(12, Pin.OUT)

# Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("WIFI_SI1", "wifisi01")

while not wifi.isconnected():
    time.sleep(1)

print("IP :", wifi.ifconfig()[0])

# Serveur
serveur = socket.socket()
serveur.bind(("0.0.0.0", 80))
serveur.listen(1)

# Page HTML
with open("index.html", "r") as fichier:
    html = fichier.read()

while True:

    client, adresse = serveur.accept()
    requete = client.recv(1024)

    # Connexion WebSocket
    if b"Upgrade: websocket" in requete:

        lignes = requete.split(b"\r\n")

        for ligne in lignes:
            if b"Sec-WebSocket-Key:" in ligne:
                cle = ligne.split(b": ")[1]

        # Création de la clé WebSocket
        magic = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        sha1 = uhashlib.sha1(cle + magic).digest()
        accept = ubinascii.b2a_base64(sha1).strip()

        client.send(
            b"HTTP/1.1 101 Switching Protocols\r\n"
            b"Upgrade: websocket\r\n"
            b"Connection: Upgrade\r\n"
            b"Sec-WebSocket-Accept: " + accept + b"\r\n\r\n"
        )

        print("WebSocket connecté")

        ancien = -1

        while True:

            etat = button.value()

            if etat != ancien:

                ancien = etat

                if etat == 1:
                    led.value(1)
                    message = "APPUYE,ALLUMEE"
                else:
                    led.value(0)
                    message = "RELACHEE,ETEINTE"

                # Envoyer le message
                data = message.encode()

                trame = bytearray([0x81, len(data)])
                trame.extend(data)

                client.send(trame)

            time.sleep(0.1)

    else:

        # Envoyer la page HTML
        client.send(
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/html\r\n\r\n"
        )

        client.send(html.encode())

    client.close()