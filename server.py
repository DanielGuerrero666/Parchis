import time
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

players = {
    "red": None,
    "yellow": None,
    "green": None,
    "blue": None,
    "black": None,
    "brown": None,
    "gray": None,
    "orange": None,
    "pink": None,
    "purple": None,
    "white": None,
    "turquoise": None,
    "olive-green": None,
    "mint-green": None,
    "burgundy": None,
    "magenta": None,
    "salmon": None,
    "cyan": None,
    "beige": None,
    "rose": None,
    "dark-green": None,
    "olive": None,
    "lilac": None,
    "fuchsia": None,
    "mustard": None,
    "ochre": None,
    "teal": None,
    "mauve": None,
    "dark-purple": None,
    "lime-green": None,
    "light-green": None,
    "plum": None,
    "light-blue": None,
    "peach": None,
    "violet": None
}

playercounter = 0

while True:
    # Saluda a un nuevo jugador que ha entrado al servidor
    #print("Server status: ON")
    #primer recv
    message = socket.recv_json() #recibe el nombre del usuario 
    name = json.loads(message)
    for key in players:
        if players[key] is None:
            players[key] = message
            playercounter += 1
            break

    message = json.dumps("Estas en linea, esperando jugadores...")
    socket.send_json(message)
    

    """# Espera a que se haya suficientes jugadores para iniciar la partida
    if len(players) > 1:
        print("Iniciando partida...")
        socket.send(b"Iniciando partida...")
        break
    elif len(players) < 2:
        print("Esperando a otro jugador...")
        message = socket.recv()
        print(f"Bienvenido jugador: {message}")
        players.append(message)
        print(f"Jugadores conectados: {players}")
        socket.send(b"Jugador conectado")"""
    
    