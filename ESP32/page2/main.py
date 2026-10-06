python
import network
import time
from machine import Pin

try:
    import usocket as socket
except:
    import socket



# LED


pin12 = Pin(12, Pin.OUT)



# Bouton physique


button = Pin(35, Pin.IN, Pin.PULL_UP)


# État de la LED


etat_led = False

pin12.value(0)



# Page HTML


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

print(
    "Le serveur écoute à l'adresse IP =",
    wlan.ifconfig()[0],
    "sur le port 80"
)



# Serveur


s = socket.socket()

ai = socket.getaddrinfo("0.0.0.0", 80)

addr = ai[0][-1]

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(addr)

s.listen(5)



# Boucle principale


while True:

    # Bouton physique
    

    if button.value() == 0:

        etat_led = True

    else:

        etat_led = False


    # On applique l'état à la LED

    pin12.value(etat_led)


    
    # Attente d'une requête
    

    s.settimeout(0.1)

    try:

        res = s.accept()

        client_s = res[0]

        requete = client_s.recv(4096)

        print("Requête reçue =", requete)


       
        # Bouton du site
       

        if b"GET /changer" in requete:

            etat_led = not etat_led

            pin12.value(etat_led)


        # Demande de l'état
       

        if b"GET /etat" in requete:

            if etat_led:

                reponse = "1"

            else:

                reponse = "0"


            client_s.send(b"HTTP/1.1 200 OK\r\n")
            client_s.send(b"Content-Type: text/plain\r\n")
            client_s.send(b"Connection: close\r\n")
            client_s.send(b"\r\n")

            client_s.send(reponse.encode())

            client_s.close()

            continue


        # Envoi de la page HTML


        client_s.send(b"HTTP/1.1 200 OK\r\n")
        client_s.send(b"Content-Type: text/html\r\n")
        client_s.send(b"Connection: close\r\n")
        client_s.send(b"\r\n")

        client_s.send(html.encode())

        client_s.close()


    except:

        pass
