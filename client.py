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
        decision = input("Do you want to add the results? (Type 'yes' or 'no'): ")
        if decision.strip().lower() == "yes":
            message = {"action": "move", "client_id": client_id, "dice_roll1": dice_roll1, "dice_roll2": dice_roll2}
            socket.send_json(message)
            response = socket.recv_json()
            print("Your new position is: {}".format(response["position"]))
        else:
            print("Skipped adding dice results.")
        time.sleep(1)

if __name__ == "__main__":
    main()
