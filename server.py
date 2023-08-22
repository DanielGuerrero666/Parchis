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

    players = []
    current_turn = 0

    while True:
        message = socket.recv_json()

        if message["action"] == "register":
            client_id = message["client_id"]
            if len(players) < 4:
                players.append({
                    "id": client_id,
                    "positions": [0, 0, 0, 0],
                    "heaven_pieces": 0,
                    "consecutive_even": 0,
                    "last_even": False,
                    "color": len(players)  # Assign a color based on the number of registered players
                })
                socket.send_string("Registered successfully!")
            else:
                socket.send_string("The game is full. Cannot register more players.")

        elif message["action"] == "move":
            client_id = message["client_id"]
            if players[current_turn]["id"] == client_id:
                target_player = next(player for player in players if player["id"] == client_id)
                piece_indices = message.get("piece_indices", [])
                dice_roll1 = message["dice_roll1"]
                dice_roll2 = message["dice_roll2"]
                total_roll = dice_roll1 + dice_roll2

                if len(piece_indices) > 1:
                    new_position = dice_roll1
                    new_position2 = dice_roll2
                else:
                    new_position = total_roll

                if target_player["last_even"]:
                    target_player["last_even"] = False
                    target_player["consecutive_even"] = 0
                    new_position += target_player["positions"][piece_indices[0]]
                else:
                    new_position += target_player["positions"][piece_indices[0]]
                    if len(piece_indices) > 1:
                        new_position2 += target_player["positions"][piece_indices[1]]

                if total_roll % 2 == 0:
                    target_player["consecutive_even"] += 1
                    if target_player["consecutive_even"] == MAX_CONSECUTIVE_EVEN:
                        max_position = max(new_position - total_roll, target_player["positions"][piece_indices[0]])
                        if len(piece_indices) > 1:
                            max_position = max(max_position, target_player["positions"][piece_indices[1]])
                        new_position = check_eat(target_player["positions"], max_position)
                        new_position = check_zone(new_position)
                        new_position = check_safe_zone(new_position)
                        target_player["positions"][piece_indices[0]] = new_position
                        if len(piece_indices) > 1:
                            target_player["positions"][piece_indices[1]] = new_position2
                        socket.send_json({"positions": target_player["positions"], "heaven_pieces": target_player["heaven_pieces"]})
                    else:
                        target_player["last_even"] = True
                        new_position = check_eat(target_player["positions"], new_position)
                        new_position = check_zone(new_position)
                        new_position = check_safe_zone(new_position)
                        target_player["positions"][piece_indices[0]] = new_position
                        if len(piece_indices) > 1:
                            target_player["positions"][piece_indices[1]] = new_position2
                        socket.send_json({"positions": target_player["positions"], "heaven_pieces": target_player["heaven_pieces"]})
                else:
                    target_player["consecutive_even"] = 0
                    target_player["last_even"] = False
                    new_position = check_eat(target_player["positions"], new_position)
                    new_position = check_zone(new_position)
                    new_position = check_safe_zone(new_position)
                    target_player["positions"][piece_indices[0]] = new_position
                    if len(piece_indices) > 1:
                        target_player["positions"][piece_indices[1]] = new_position2
                    if check_win(target_player["positions"]):
                        target_player["heaven_pieces"] += 1
                        target_player["positions"][piece_indices[0]] = -1
                        if len(piece_indices) > 1:
                            target_player["positions"][piece_indices[1]] = -1
                    socket.send_json({"positions": target_player["positions"], "heaven_pieces": target_player["heaven_pieces"]})
                current_turn = (current_turn + 1) % len(players)
            else:
                socket.send_string("Not your turn.")    
        elif message["action"] == "get_turn":
            socket.send_string(players[current_turn]["id"])  # Send the current turn to the client
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
    zone_position = position % ZONE_SIZE
    if zone_position in SAFE_ZONE_POSITIONS and zone_position != SAFE_ZONE_OFFSET:
        return position
    return check_zone(position)

def check_win(positions):
    return all(pos == ZONE_SIZE * 4 + HEAVENS_PATH_LENGTH for pos in positions)

if __name__ == "__main__":
    main()
