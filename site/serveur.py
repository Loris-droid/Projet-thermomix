from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

etape = 0
etapes = [
    {"titre": "Ajouter les ingrédients", "description": "Placez tous les ingrédients dans le bol.", "temps": "00:00", "temperature": "0 °C", "vitesse": "0"},
    {"titre": "Mélanger", "description": "Mélange des ingrédients.", "temps": "00:30", "temperature": "0 °C", "vitesse": "4"},
    {"titre": "Cuisson", "description": "Cuisson de la préparation.", "temps": "05:00", "temperature": "100 °C", "vitesse": "2"},
    {"titre": "Terminé", "description": "La recette est terminée !", "temps": "00:00", "temperature": "0 °C", "vitesse": "0"}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/thermomix")
def thermomix():
    return render_template("thermomix.html")

@socketio.on("connect")
def connexion():
    socketio.emit("etape", {"numero": etape, "total": len(etapes), "contenu": etapes[etape]})

@socketio.on("suivant")
def suivant():
    global etape
    if etape < len(etapes) - 1:
        etape = etape + 1
    envoyer_etape()

@socketio.on("precedent")
def precedent():
    global etape
    if etape > 0:
        etape = etape - 1
    envoyer_etape()

def envoyer_etape():
    socketio.emit("etape", {"numero": etape, "total": len(etapes), "contenu": etapes[etape]})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
