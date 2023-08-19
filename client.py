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
        dice_roll = random.randint(1, 6)
        message = {"action": "move", "client_id": client_id, "dice_roll": dice_roll}
        socket.send_json(message)
        response = socket.recv_json()
        print("You rolled a {}. Your new position is: {}".format(dice_roll, response["position"]))
        time.sleep(1)

if __name__ == "__main__":
    main()
