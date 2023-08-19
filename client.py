import zmq
import time
import random

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
        print("Your new positions are: {}".format(response["positions"]))
        time.sleep(1)

if __name__ == "__main__":
    main()
