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
                piece_indices = message.get("piece_indices", [])
                dice_roll1 = message["dice_roll1"]
                dice_roll2 = message["dice_roll2"]
                
                if len(piece_indices) == 1:
                    piece_index = piece_indices[0]
                    if 0 <= piece_index < 4:
                        total_roll = dice_roll1 + dice_roll2
                        target_player["positions"][piece_index] += total_roll
                        socket.send_json({"positions": target_player["positions"]})
                    else:
                        socket.send_string("Invalid piece index.")
                elif len(piece_indices) == 2:
                    piece_index1 = piece_indices[0]
                    piece_index2 = piece_indices[1]
                    if 0 <= piece_index1 < 4 and 0 <= piece_index2 < 4 and piece_index1 != piece_index2:
                        target_player["positions"][piece_index1] += dice_roll1
                        target_player["positions"][piece_index2] += dice_roll2
                        socket.send_json({"positions": target_player["positions"]})
                    else:
                        socket.send_string("Invalid piece indices.")
                else:
                    socket.send_string("Invalid number of piece indices.")
            else:
                socket.send_string("Player {} not registered.".format(client_id))

        else:
            socket.send_string("Unknown action.")

if __name__ == "__main__":
    main()
