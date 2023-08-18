import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Conectando al servidor...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Datos del usuario
playing = True
name = "Test_Player"

while playing:
    print("Bienvenido jugador" '\n')
    name = input("Por favor ingrese su nombre de usuario: ")
    nameJson = json.dumps(name)
    socket.send_json(nameJson)

    message = socket.recv()
    message = json.loads(message)
    print(message)
    playing = False

    #Aqui es donde se tiene que estar mandando mensajes al servidor 
    #Preguntando si ya esta listo el juego