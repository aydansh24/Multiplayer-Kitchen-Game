from station import Station
from plate import Plate

class Stove(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cooking = False
        self.cook_time = 0

    def interact(self, player):
        # Place raw patty on stove
        if player.inventory is not None and self.item is None:
            if player.inventory.name == "patty_raw":
                self.item = player.inventory
                player.inventory = None
                self.cooking = True
                self.cook_time = 0

        # Pick up cooked patty — empty hand
        elif player.inventory is None and self.item is not None:
            player.inventory = self.item
            self.item = None
            self.cooking = False
            self.cook_time = 0

        # Pick up cooked patty directly onto held plate
        elif isinstance(player.inventory, Plate) and self.item is not None:
            player.inventory.add_ingredient(self.item)
            self.item = None
            self.cooking = False
            self.cook_time = 0

    def update(self):
        if self.cooking and self.item:
            self.cook_time += 1
            if self.cook_time > 180:
                self.item.name = "patty_cooked"
                self.cooking = False