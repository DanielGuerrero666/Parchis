import zmq

ZONE_SIZE = 14
SAFE_ZONE_POSITIONS = [7, 14]
SAFE_ZONE_OFFSET = 5
HEAVENS_PATH_LENGTH = 7
MAX_CONSECUTIVE_EVEN = 3

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    players = {}

    while True:
        message = socket.recv_json()

        if message["action"] == "register":
            client_id = message["client_id"]
            players[client_id] = {
                "positions": [0, 0, 0, 0],
                "heaven_pieces": 0,
                "consecutive_even": 0,
                "last_even": False
            }
            socket.send_string("Registered successfully!")

        elif message["action"] == "move":
            client_id = message["client_id"]
            target_player = players.get(client_id)
            if target_player:
                piece_indices = message.get("piece_indices", [])
                dice_roll1 = message["dice_roll1"]
                dice_roll2 = message["dice_roll2"]
                
                total_roll = dice_roll1 + dice_roll2
                new_position = total_roll
                if target_player["last_even"]:
                    target_player["last_even"] = False
                    target_player["consecutive_even"] = 0
                    new_position += target_player["positions"][piece_indices[0]]
                else:
                    new_position += target_player["positions"][piece_indices[0]]
                    new_position += target_player["positions"][piece_indices[1]]
                
                if total_roll % 2 == 0:
                    target_player["consecutive_even"] += 1
                    if target_player["consecutive_even"] == MAX_CONSECUTIVE_EVEN:
                        max_position = max(new_position - total_roll, target_player["positions"][piece_indices[0]])
                        max_position = max(max_position, target_player["positions"][piece_indices[1]])
                        new_position = check_eat(target_player["positions"], max_position)
                        new_position = check_zone(new_position)
                        new_position = check_safe_zone(new_position)
                        target_player["positions"][piece_indices[0]] = new_position
                        target_player["positions"][piece_indices[1]] = new_position
                        socket.send_json({"positions": target_player["positions"], "heaven_pieces": target_player["heaven_pieces"]})
                    else:
                        target_player["last_even"] = True
                        new_position = check_eat(target_player["positions"], new_position)
                        new_position = check_zone(new_position)
                        new_position = check_safe_zone(new_position)
                        target_player["positions"][piece_indices[0]] = new_position
                        target_player["positions"][piece_indices[1]] = new_position
                        socket.send_json({"positions": target_player["positions"], "heaven_pieces": target_player["heaven_pieces"]})
                else:
                    target_player["consecutive_even"] = 0
                    target_player["last_even"] = False
                    new_position = check_eat(target_player["positions"], new_position)
                    new_position = check_zone(new_position)
                    new_position = check_safe_zone(new_position)
                    target_player["positions"][piece_indices[0]] = new_position
                    target_player["positions"][piece_indices[1]] = new_position
                    if check_win(target_player["positions"]):
                        target_player["heaven_pieces"] += 1
                        target_player["positions"][piece_indices[0]] = -1
                        target_player["positions"][piece_indices[1]] = -1
                    socket.send_json({"positions": target_player["positions"], "heaven_pieces": target_player["heaven_pieces"]})
            else:
                socket.send_string("Player {} not registered.".format(client_id))

        else:
            socket.send_string("Unknown action.")

# The rest of the code remains unchanged...

if __name__ == "__main__":
    main()
