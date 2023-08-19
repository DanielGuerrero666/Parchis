import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    clients = {}

    while True:
        message = socket.recv_json()

        if message["action"] == "register":
            client_id = message["client_id"]
            clients[client_id] = socket
            socket.send_string("Registered successfully!")

        elif message["action"] == "move":
            client_id = message["client_id"]
            target_client = clients.get(client_id)
            if target_client:
                move_data = message["move_data"]
                target_client.send_json(move_data)
                socket.send_string("Move sent to client {}".format(client_id))
            else:
                socket.send_string("Client {} not registered.".format(client_id))

        else:
            socket.send_string("Unknown action.")

if __name__ == "__main__":
    main()
