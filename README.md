# Burnt Exceptions
This is a multiplayer cooking game built with Python and Pygame, inspired by Overcooked and PlateUp. Work together with up to 4 players to prepare and serve burger orders before time runs out.

---

## Requirements

- Python 3.10+
- Pygame (`pip install pygame`)
- All players must be on the same local network

---

## How to Run

**Start the server** (one machine only):
```
python server.py
```

**Start the client** (every player, including the host):
```
python client.py
```

Before running, set the `server` IP in `network.py` to the host machine's local IP address. On Windows, find it by running `ipconfig` in the command prompt and looking for the WiFi adapter IP (e.g. `192.168.1.x`).

---

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move |
| C | Pick up / place items, interact with stations |
| X | Cut ingredient at the cutting station |

---

## Gameplay

### Objective
Complete as many burger orders as possible within 1 minute 30 seconds. Each ingredient on a completed order earns $100.

### Order Types
| Order | Image | Ingredients |
|-------|-------|-------------|
| Plain Burger | ![](/Multiplayer/sprites/ingredients/burger.png) | Patty + Bun |
| Lettuce Burger | ![](/Multiplayer/sprites/ingredients/burger_lettuce.png) | Patty + Sliced Lettuce + Bun |
| Tomato Burger | ![](/Multiplayer/sprites/ingredients/burger_tomato.png) | Patty + Sliced Tomato + Bun |
| Full Burger | ![](/Multiplayer/sprites/ingredients/burger_tomato_lettuce.png) | Patty + Sliced Lettuce + Sliced Tomato + Bun |

### Stations
| Station | Image | Description |
|---------|-------|-------------|
| Meat Crate | ![](/Multiplayer/sprites/stations/meat_crate.png) | Grab raw patties |
| Tomato Crate | ![](/Multiplayer/sprites/stations/tomato_crate.png) | Grab tomatoes |
| Lettuce Crate | ![](/Multiplayer/sprites/stations/lettuce_crate.png) | Grab lettuce |
| Bun Crate | ![](/Multiplayer/sprites/stations/bun_crate.png) | Grab buns |
| Stove | ![](/Multiplayer/sprites/stations/stove.png) | Cook raw patties into cooked patties (takes 3 seconds) |
| Cutting Station | ![](/Multiplayer/sprites/stations/cutting_station.png) | Cut tomatoes and lettuce (press X) |
| Plate Station | ![](/Multiplayer/sprites/stations/plate_station.png) | Grab a clean plate |
| Counter | ![](/Multiplayer/sprites/stations/counter_front.png) | Place and pick up items, assemble ingredients onto plates |
| Submit Station | ![](/Multiplayer/sprites/stations/submit_station.png) | Submit a completed plate to fulfill an order |
| Trash | ![](/Multiplayer/sprites/stations/trash.png) | Discard all held items |

---

## Lobby

- The first player to connect becomes the **Host**
- Other players click **Ready** when they are ready
- The Host can click **Start Game** once all players are ready (minimum 2 players by default)

---

## Project Structure

```
├── client.py           # Main client — rendering, input, game loop
├── server.py           # Game server — state management, networking
├── network.py          # Client-side networking
├── player.py           # Player class
├── station.py          # Base station class
├── counter.py          # Counter station
├── crate.py            # Ingredient crate
├── cutting_station.py  # Cutting station
├── stove.py            # Stove station
├── plate_station.py    # Plate dispenser
├── submit_station.py   # Order submission station
├── trash.py            # Trash station
├── plate.py            # Plate class with burger image logic
├── ingredient.py       # Ingredient class
├── order.py            # Order generation and matching
├── ui.py               # All UI drawing (menu, lobby, HUD, end screen)
├── sprites/            # All game sprites
└── sounds/             # Sound effects and background music
```

---

## Notes

- Only ingredients that are properly prepared (cooked patty, sliced vegetables, bun) can be placed on a plate
- Raw or uncut ingredients cannot be plated
- New orders spawn every 10 seconds, up to a maximum of 5 at once
