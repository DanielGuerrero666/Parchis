import zmq

context = zmq.Context()

#  Socket to talk to server
print("Conectando al servidor...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Datos del usuario
playing = True
name = "Test_Player"

while playing:
    socket.send(b"Test_Player")

    message = socket.recv()
    print(f"[{message}]")