import zmq
import time

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    client_id = input("Enter your client ID: ")
    message = {"action": "register", "client_id": client_id}
    socket.send_json(message)
    response = socket.recv_string()
    print(response)

    while True:
        move_data = input("Enter move data: ")
        message = {"action": "move", "client_id": client_id, "move_data": move_data}
        socket.send_json(message)
        response = socket.recv_string()
        print(response)
        time.sleep(1)

if __name__ == "__main__":
    main()
