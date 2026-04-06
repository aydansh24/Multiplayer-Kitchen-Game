from station import Station

class Trash(Station):
    def interact(self, player):
        if player.inventory:
            player.inventory = None