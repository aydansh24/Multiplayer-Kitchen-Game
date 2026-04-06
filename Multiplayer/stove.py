from station import Station

class Stove(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cooking = False
        self.cook_time = 0

    def interact(self, player):
        if player.inventory and self.item is None:
            if player.inventory.name == "patty_raw":
                self.item = player.inventory
                player.inventory = None
                self.cooking = True
                self.cook_time = 0
        elif player.inventory is None and self.item:
            player.inventory = self.item
            self.item = None
            self.cooking = False
            self.cook_time = 0

    def update(self):
        if self.cooking and self.item:
            self.cook_time += 1
            if self.cook_time > 180:  # 3 seconds at 60 FPS
                self.item.name = "patty_cooked"
                self.cooking = False