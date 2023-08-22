import zmq
import time
import random

ZONE_SIZE = 14
SAFE_ZONE_POSITIONS = [7, 14]
SAFE_ZONE_OFFSET = 5

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
        socket.send_json({"action": "get_turn"})  # Request the current turn from the server
        current_turn = socket.recv_string()  # Receive the current turn from the server

        if current_turn == client_id:
            input("Press Enter to roll the dice...")
            dice_roll1 = random.randint(1, 6)
            dice_roll2 = random.randint(1, 6)
            print("You rolled {} and {}.".format(dice_roll1, dice_roll2))

            decision = input("Do you want to move 1 piece or 2 pieces? (Type '1' or '2'): ")
            if decision.strip() == "1":
                piece_index = int(input("Choose a piece to move (0-3): "))
                message = {
                    "action": "move",
                    "client_id": client_id,
                    "piece_indices": [piece_index],
                    "dice_roll1": dice_roll1,
                    "dice_roll2": dice_roll2
                }
            elif decision.strip() == "2":
                piece_index1 = int(input("Choose the first piece to move (0-3): "))
                piece_index2 = int(input("Choose the second piece to move (0-3, different from the first piece): "))
                message = {
                    "action": "move",
                    "client_id": client_id,
                    "piece_indices": [piece_index1, piece_index2],
                    "dice_roll1": dice_roll1,
                    "dice_roll2": dice_roll2
                }
            else:
                print("Invalid input. Please enter '1' or '2'.")
                continue

            socket.send_json(message)
            response = socket.recv_json()
            show_positions(client_id, response["positions"], response["heaven_pieces"])
        else:
            print("Wait for your turn...")

        time.sleep(5)  # Tiempo de espera antes de consultar turno nuevamente

def show_positions(client_id, positions, heaven_pieces):
    zone_names = ["Red", "Blue", "Green", "Yellow"]
    for idx, pos in enumerate(positions):
        zone_name = zone_names[idx // 4]
        zone_position = pos % ZONE_SIZE
        safe_zone_text = "Safe" if zone_position in SAFE_ZONE_POSITIONS else ""
        print("Player {}: Piece {} is now in {}:{}{}, Heaven pieces: {}".format(client_id, idx, zone_name, safe_zone_text, zone_position, heaven_pieces))

if __name__ == "__main__":
    main()
