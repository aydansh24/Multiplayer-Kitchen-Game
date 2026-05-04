## Multiplayer Kitchen game
This is a multiplayer cooking simulator game in Python, where 2-4 players work together to complete various orders and accumulate the highest score

## Installation Requirements
For this game, you and other players will need to have pygame installed. Use the following command in the terminal to install pygame
```bash
pip install pygame
```

## How to Play
1. All players must be connected to the same network
2. All players must download all files in the "Multiplayer" folder
3. In "network.py", all players must change "self.server" to one person's IP Address. This person will be the designated host of this game.

# Host
1. To find the host's IP Address, in your terminal, type
```bash
ipconfig
```
2. Underneath "Wireless LAN Adapter Wifi", copy and paste the IPv4 Address into "self.server" in "network.py"
3. All players should have the same address in their "self.server"
