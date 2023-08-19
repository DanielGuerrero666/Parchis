import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    players = {}

    while True:
        message = socket.recv_json()

        if message["action"] == "register":
            client_id = message["client_id"]
            players[client_id] = {"positions": [0, 0, 0, 0]}
            socket.send_string("Registered successfully!")

        elif message["action"] == "move":
            client_id = message["client_id"]
            target_player = players.get(client_id)
            if target_player:
                piece_index = message["piece_index"]
                if 0 <= piece_index < 4:
                    socket.send_string("Roll the dice. Type 'add' to add the results, or 'skip' to skip.")
                    response = socket.recv_string()
                    if response.strip().lower() == "add":
                        dice_roll1 = message["dice_roll1"]
                        dice_roll2 = message["dice_roll2"]
                        total_roll = dice_roll1 + dice_roll2
                        target_player["positions"][piece_index] += total_roll
                    else:
                        socket.send_string("Skipped adding dice results.")
                    socket.send_json({"positions": target_player["positions"]})
                else:
                    socket.send_string("Invalid piece index.")
            else:
                socket.send_string("Player {} not registered.".format(client_id))

        else:
            socket.send_string("Unknown action.")

if __name__ == "__main__":
    main()
