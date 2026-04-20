import pickle
import socket
from _thread import start_new_thread
from player import Player
from plate import Plate
from crate import Crate
from counter import Counter
from trash import Trash
from stove import Stove
from plate_station import PlateStation
from submit_station import SubmitStation
from order import Order

server = "0.0.0.0"
port = 5555
MAX_PLAYERS = 4
MIN_PLAYERS_TO_START = 2
MAX_ORDERS = 3
ORDER_INTERVAL = 600  # 10 seconds at 60 fps

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def make_players():
    return [
        Player(0, 30, "red"),
        Player(200, 50, "yellow"),
        Player(50, 200, "green"),
        Player(200, 200, "blue")
    ]


def make_stations():
    return [
        Crate(96, 0, "tomato_crate"),
        Crate(480, 480, "lettuce_crate"),
        Crate(0, 576, "meat_crate"),
        Counter(288, 384),
        Counter(96, 384),
        Counter(384, 288),
        Trash(576, 576),
        Stove(672, 384),
        PlateStation(864, 192),
        SubmitStation(864, 480)
    ]


def reset_world():
    global players, stations, orders, order_timer
    players = make_players()
    stations = make_stations()
    orders = [Order()]
    order_timer = 0


players = []
stations = []
orders = []
order_timer = 0
reset_world()

connected_players = set()
ready_players = set()
host_id = None
game_started = False
room_broken = False


def next_available_player_id():
    for i in range(MAX_PLAYERS):
        if i not in connected_players:
            return i
    return None


def build_lobby_state(player_id):
    return {
        "type": "lobby",
        "player_id": player_id,
        "host_id": host_id,
        "connected_players": sorted(list(connected_players)),
        "ready_players": sorted(list(ready_players)),
        "game_started": game_started,
        "room_broken": room_broken,
        "min_players_to_start": MIN_PLAYERS_TO_START
    }


def can_start_game():
    if len(connected_players) < MIN_PLAYERS_TO_START:
        return False

    for pid in connected_players:
        if pid != host_id and pid not in ready_players:
            return False

    return True


def cleanup_player(player_id):
    global host_id, game_started, room_broken

    connected_players.discard(player_id)
    ready_players.discard(player_id)

    if player_id == host_id:
        if connected_players:
            host_id = min(connected_players)
        else:
            host_id = None

    if len(connected_players) == 0:
        ready_players.clear()
        game_started = False
        room_broken = False
        reset_world()


try:
    s.bind((server, port))
    print(f"Server bound to {server}:{port}")
except socket.error as e:
    print("Bind failed:", e)
    raise

s.listen(MAX_PLAYERS)
print("Waiting for connection... Server Started")


def threaded_client(conn, player_id):
    global host_id, game_started, room_broken, order_timer, players, stations, orders

    if host_id is None:
        host_id = player_id

    connected_players.add(player_id)

    try:
        conn.send(pickle.dumps(player_id))

        while True:
            data = conn.recv(8192)
            if not data:
                break

            data = pickle.loads(data)
            mode = data.get("mode")

            if mode == "lobby":
                action = data.get("action")

                if room_broken:
                    conn.sendall(pickle.dumps(build_lobby_state(player_id)))
                    continue

                if action == "ready":
                    if player_id != host_id:
                        if player_id in ready_players:
                            ready_players.remove(player_id)
                        else:
                            ready_players.add(player_id)

                elif action == "start_game":
                    if player_id == host_id and can_start_game():
                        game_started = True
                        room_broken = False
                        reset_world()

                elif action == "break_room":
                    if player_id == host_id:
                        room_broken = True
                        game_started = False

                reply = build_lobby_state(player_id)
                conn.sendall(pickle.dumps(reply))

            elif mode == "game":
                if room_broken or not game_started:
                    conn.sendall(pickle.dumps(build_lobby_state(player_id)))
                    continue

                player_obj = data["player"]
                action = data["action"]

                players[player_id] = player_obj

                # In the interact block in server.py, replace with:
                if action == "interact":
                    hand_rect = player_obj.get_hand_rect()
                    for st in stations:
                        if hand_rect.colliderect(st.rect):
                            if st.__class__.__name__ == "SubmitStation":
                                if isinstance(player_obj.inventory, Plate) and not player_obj.inventory.is_empty():
                                    for order in orders[:]:
                                        if order.matches(player_obj.inventory):
                                            orders.remove(order)
                                            player_obj.inventory = None
                                            break
                            else:
                                st.interact(player_obj)

                if action == "submit":
                    if isinstance(player_obj.inventory, Plate):
                        for order in orders[:]:
                            if order.matches(player_obj.inventory):
                                orders.remove(order)
                                player_obj.inventory = None
                                break

                order_timer += 1
                if order_timer >= ORDER_INTERVAL and len(orders) < MAX_ORDERS:
                    orders.append(Order())
                    order_timer = 0

                for st in stations:
                    if hasattr(st, "update"):
                        st.update()

                reply = {
                    "type": "game",
                    "players": players,
                    "stations": stations,
                    "orders": orders
                }
                conn.sendall(pickle.dumps(reply))

            else:
                conn.sendall(pickle.dumps({"type": "error", "message": "Unknown mode"}))

    except Exception as e:
        print(f"Player {player_id} disconnected/error:", e)

    finally:
        conn.close()
        cleanup_player(player_id)


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    player_id = next_available_player_id()
    if player_id is None:
        conn.close()
        continue

    start_new_thread(threaded_client, (conn, player_id))