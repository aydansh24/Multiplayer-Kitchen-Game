import pickle
import socket
from _thread import *
from player import Player

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
    Player(0, 0, 60, 96, (255, 0, 0)),
    Player(200, 50, 50, 50, (0, 255, 0)),
    Player(50, 200, 50, 50, (0, 0, 255)),
    Player(200, 200, 50, 50, (255, 255, 0))
]


def threaded_client(conn, player):
    conn.send(pickle.dumps(player))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Disconnected")
                break
            else:
                players[player] = data
                reply = players

            conn.sendall(pickle.dumps(reply))

        except:
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


