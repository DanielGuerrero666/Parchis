import zmq

ZONE_SIZE = 14
SAFE_ZONE_POSITIONS = [7, 14]
SAFE_ZONE_OFFSET = 5
HEAVENS_PATH_LENGTH = 7

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    players = {}

    while True:
        message = socket.recv_json()

        if message["action"] == "register":
            client_id = message["client_id"]
            players[client_id] = {"positions": [0, 0, 0, 0], "heaven_pieces": 0}
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
                        new_position = target_player["positions"][piece_index] + total_roll
                        new_position = check_eat(target_player["positions"], new_position)
                        new_position = check_zone(new_position)
                        new_position = check_safe_zone(new_position)
                        target_player["positions"][piece_index] = new_position
                        if check_win(target_player["positions"]):
                            target_player["heaven_pieces"] += 1
                            target_player["positions"][piece_index] = -1
                        socket.send_json({"positions": target_player["positions"], "heaven_pieces": target_player["heaven_pieces"]})
                    else:
                        socket.send_string("Invalid piece index.")
                elif len(piece_indices) == 2:
                    piece_index1 = piece_indices[0]
                    piece_index2 = piece_indices[1]
                    if 0 <= piece_index1 < 4 and 0 <= piece_index2 < 4 and piece_index1 != piece_index2:
                        new_position1 = target_player["positions"][piece_index1] + dice_roll1
                        new_position2 = target_player["positions"][piece_index2] + dice_roll2
                        new_position1 = check_eat(target_player["positions"], new_position1)
                        new_position2 = check_eat(target_player["positions"], new_position2)
                        new_position1 = check_zone(new_position1)
                        new_position2 = check_zone(new_position2)
                        new_position1 = check_safe_zone(new_position1)
                        new_position2 = check_safe_zone(new_position2)
                        target_player["positions"][piece_index1] = new_position1
                        target_player["positions"][piece_index2] = new_position2
                        if check_win(target_player["positions"]):
                            target_player["heaven_pieces"] += 1
                            target_player["positions"][piece_index1] = -1
                            target_player["positions"][piece_index2] = -1
                        socket.send_json({"positions": target_player["positions"], "heaven_pieces": target_player["heaven_pieces"]})
                    else:
                        socket.send_string("Invalid piece indices.")
                else:
                    socket.send_string("Invalid number of piece indices.")
            else:
                socket.send_string("Player {} not registered.".format(client_id))

        else:
            socket.send_string("Unknown action.")

def check_eat(positions, new_position):
    for idx, pos in enumerate(positions):
        if pos != 0 and pos == new_position:
            return idx * -1
    return new_position

def check_zone(position):
    if position >= ZONE_SIZE * 4:
        return position - ZONE_SIZE * 4
    return position

def check_safe_zone(position):
    zone_index = position // ZONE_SIZE
    zone_position = position % ZONE_SIZE
    if zone_position in SAFE_ZONE_POSITIONS and zone_position != SAFE_ZONE_OFFSET:
        return position
    return check_zone(position)

def check_win(positions):
    return all(pos == ZONE_SIZE * 4 + HEAVENS_PATH_LENGTH for pos in positions)

if __name__ == "__main__":
    main()
