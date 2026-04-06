from station import Station

class Counter(Station):
    def interact(self, player):
        if player.inventory and self.item is None:
            self.item = player.inventory
            player.inventory = None
        elif player.inventory is None and self.item:
            player.inventory = self.item
            self.item = None