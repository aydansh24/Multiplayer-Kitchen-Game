import pickle
import socket
from _thread import *
from player import Player
from crate import Crate
from counter import Counter
from trash import Trash
from stove import Stove
from plate_station import PlateStation

server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for connection... Server Started")

"""
Tiles
[(0, 0),   (96, 0),   (192, 0),   (288, 0),   (384, 0),   (480, 0),   (576, 0),   (672, 0),   (768, 0),   (864, 0)]
[(0, 96),  (96, 96),  (192, 96),  (288, 96),  (384, 96),  (480, 96),  (576, 96),  (672, 96),  (768, 96),  (864, 96)]
[(0, 192), (96, 192), (192, 192), (288, 192), (384, 192), (480, 192), (576, 192), (672, 192), (768, 192), (864, 192)]
[(0, 288), (96, 288), (192, 288), (288, 288), (384, 288), (480, 288), (576, 288), (672, 288), (768, 288), (864, 288)]
[(0, 384), (96, 384), (192, 384), (288, 384), (384, 384), (480, 384), (576, 384), (672, 384), (768, 384), (864, 384)]
[(0, 480), (96, 480), (192, 480), (288, 480), (384, 480), (480, 480), (576, 480), (672, 480), (768, 480), (864, 480)]
[(0, 576), (96, 576), (192, 576), (288, 576), (384, 576), (480, 576), (576, 576), (672, 576), (768, 576), (864, 576)]
"""

players = [
    Player(0, 30, (255, 0, 0)),
    Player(200, 50, (0, 255, 0)),
    Player(50, 200, (0, 0, 255)),
    Player(200, 200, (255, 255, 0))
]

stations = [
    Crate(96, 0, "tomato_crate"),
    Crate(480, 480, "lettuce_crate"),
    Crate(0, 576, "meat_crate"),
    Counter(288, 384),
    Counter(96, 384),
    Counter(384, 288),
    Trash(576, 576),
    Stove(672, 384),
    PlateStation(864, 192)
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
                hand_rect = player_obj.get_hand_rect()
                for s in stations:
                    if hand_rect.colliderect(s.rect):
                        s.interact(player_obj)

            for s in stations:
                if hasattr(s, "update"):
                    s.update()

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