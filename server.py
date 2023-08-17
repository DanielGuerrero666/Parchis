import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

players = []

while True:
    # Saluda a un nuevo jugador que ha entrado al servidor
    print("Server status: ON")
    message = socket.recv()

    print(f"Bienvenido jugador: {message}")
    players.append(message)
    print(f"Jugadores conectados: {players}")
    socket.send(b"Jugador conectado")

    # Espera a que se haya suficientes jugadores para iniciar la partida
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
        socket.send(b"Jugador conectado")