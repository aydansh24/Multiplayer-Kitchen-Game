import pickle
import socket
from _thread import *
from player import Player
from station import Station

server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for connection... Server Started")


players = [
    Player(0, 0, (255, 0, 0)),
    Player(200, 50, (0, 255, 0)),
    Player(50, 200, (0, 0, 255)),
    Player(200, 200, (255, 255, 0))
]

stations = [
    Station(100, 100, "tomato_crate"),
    Station(180, 100, "lettuce_crate"),
    Station(260, 100, "counter")
]


def threaded_client(conn, player):
    conn.send(pickle.dumps(player))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break

            player_obj = data["player"]
            action = data["action"]

            players[player] = player_obj

            if action == "interact":
                for s in stations:
                    if player_obj.get_rect().colliderect(s.rect):
                        s.interact(player_obj)

            reply = (players, stations)
            conn.sendall(pickle.dumps(reply))

        except Exception as e:
            print("Error:", e)
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    if currentPlayer < 4:
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
    else:
        conn.close()