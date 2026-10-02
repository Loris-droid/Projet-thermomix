import network
import time
import ubinascii
from machine import Pin, ADC
try :
    import usocket as socket
except :
    import socket

# On définit l'entrée analogique utilisée
capt_analog = ADC(Pin(35)) # on crée l'objet connecté sur la broche 35
capt_analog.width(ADC.WIDTH_12BIT) # Pour 4096 valeurs
capt_analog.atten(ADC.ATTN_11DB)
# Code HTML de la page Web renvoyée par le serveur
html = b"""<!DOCTYPE html>
<html>
    <head>
        <title>ESP32 capteur analogique</title>
    </head>
    <body>
        <h1>Capteur analogique I35= %s</h1>
    </body>
"""

wlan = network.WLAN(network.STA_IF)
wlan.active(True) #activation de l'interface
if not wlan.isconnected(): #on attend d'etre connecte au point d'acces
    print("Connexion au point d'accès...")
    # On demande une connexion au point d'accès
    wlan.connect("WIFI_SI1", "wifisi01")
    # Boucle d'attente...
    while not wlan.isconnected() :
        print('Connexion en cours...')
        time.sleep(0.5)
print('Station connectee au point d acces')
print('Le serveur ecoute a l adresse IP=', wlan.ifconfig()[0], 'sur le port 80') 

s = socket.socket()
ai = socket.getaddrinfo("0.0.0.0", 80) # on choisit le port 80 pour le http
addr = ai[0][-1]
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5) # on peut écouter 5 clients
while True :
    res = s.accept() # On attend la requete HTTP d'un client
    client_s = res[0]
    client_addr = res[1]
    requete= client_s.recv(4096)
    print("Adresse IP du client connecte=", client_addr)
    print("Requete recue=", requete)
    val_capt_analog=capt_analog.read()
    reponse = html % val_capt_analog
    client_s.send(b'HTTP/1.1.200 OK\r\n')
    client_s.send(b'Content-Type: text/html\r\n')
    client_s.send(b'Connection: close\r\n')
    client_s.send(b'\r\n')
    client_s.send(reponse) #code HTML envoyé au client
    client_s.close()
    print()