import network
import time
from machine import Pin

try:
    import usocket as socket
except:
    import socket



# CONFIGURATION


button = Pin(35, Pin.IN, Pin.PULL_UP)
pin12 = Pin(12, Pin.OUT)

pin12.value(0)



# CONNEXION WIFI


wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():

    print("Connexion au point d'accès...")

    wlan.connect("WIFI_SI1", "wifisi01")

    while not wlan.isconnected():
        print("Connexion en cours...")
        time.sleep(0.5)


print("Station connectée au point d'accès")
print("Adresse IP =", wlan.ifconfig()[0])



# SERVEUR


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("0.0.0.0", 80))
s.listen(1)

print("Serveur Web démarré")
print("http://" + wlan.ifconfig()[0])



# PAGE HTML


with open("index.html", "r") as file:
    html = file.read()


# BOUCLE PRINCIPALE


while True:

    print("En attente d'un client...")

    client, addr = s.accept()

    print("Client connecté :", addr)

    requete = client.recv(4096)

    print(requete)


    
    # CONNEXION WEBSOCKET
    

    if b"Upgrade: websocket" in requete:

        print("Connexion WebSocket demandée")


        # Récupérer la clé WebSocket
        lignes = requete.split(b"\r\n")

        websocket_key = None

        for ligne in lignes:

            if ligne.startswith(b"Sec-WebSocket-Key:"):

                websocket_key = ligne.split(b": ", 1)[1]

                break


        if websocket_key is None:

            client.close()

            continue


       
        # CALCUL DE LA CLE WEBSOCKET
       

        import ubinascii
        import uhashlib

        magic = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

        sha1 = uhashlib.sha1(websocket_key + magic).digest()

        accept_key = ubinascii.b2a_base64(sha1).strip()


       
        # REPONSE HANDSHAKE
   

        client.send(
            b"HTTP/1.1 101 Switching Protocols\r\n"
            b"Upgrade: websocket\r\n"
            b"Connection: Upgrade\r\n"
            b"Sec-WebSocket-Accept: " +
            accept_key +
            b"\r\n\r\n"
        )

        print("WebSocket connecté")


        # BOUCLE WEBSOCKET

        dernier_etat = -1

        while True:

            etat = button.value()


            # Détection d'un changement
            if etat != dernier_etat:

                dernier_etat = etat


                if etat == 1:

                    print("Bouton appuyé")

                    pin12.value(1)

                    message = "APPUYE,ALLUMEE"

                else:

                    print("Bouton relâché")

                    pin12.value(0)

                    message = "RELACHEE,ETEINTE"



                # CREATION D'UNE TRAME TEXT
    

                data = message.encode()

                longueur = len(data)


                if longueur < 126:

                    frame = bytearray([
                        0x81,
                        longueur
                    ])

                    frame.extend(data)

                else:

                    frame = bytearray([
                        0x81,
                        126,
                        (longueur >> 8) & 255,
                        longueur & 255
                    ])

                    frame.extend(data)


                client.send(frame)


            # Petite pause
            time.sleep(0.05)


            # Vérifier si le navigateur a envoyé quelque chose
            client.settimeout(0.01)

            try:

                donnees = client.recv(2)

                if donnees:

                    # Si le navigateur ferme la connexion
                    if donnees[0] == 0x88:

                        print("WebSocket fermé")

                        client.close()

                        break

            except:

                pass


        continue


 
    # REQUETE HTTP NORMALE


    client.send(b"HTTP/1.1 200 OK\r\n")
    client.send(b"Content-Type: text/html\r\n")
    client.send(b"Connection: close\r\n")
    client.send(b"\r\n")

    client.send(html.encode())

    client.close()