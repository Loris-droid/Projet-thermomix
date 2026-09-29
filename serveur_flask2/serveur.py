from flask import Flask, render_template
from gpiozero import LED, Button
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)

 
led = LED(17)
bouton = Button(4)

@app.route("/")
def index() :
    return render_template("index.html")

@app.route("/on")
def on() :
    led.on()
    return render_template("index.html")

@app.route("/off")
def off() :
    led.off()
    return render_template("index.html")

def envoyer_etat():
    socketio.emit('etat_bouton', bouton.is_pressed)

bouton.when_pressed = envoyer_etat
bouton.when_released = envoyer_etat


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)

