from plate import Plate
from station import Station

class Counter(Station):
    def interact(self, player):
        # Player holding plate + counter has ingredient → add ingredient to plate
        if isinstance(player.inventory, Plate) and self.item is not None and not isinstance(self.item, Plate):
            player.inventory.add_ingredient(self.item)
            self.item = None

        # Player holding ingredient + counter has plate → add ingredient to plate
        elif player.inventory is not None and not isinstance(player.inventory, Plate) and isinstance(self.item, Plate):
            self.item.add_ingredient(player.inventory)
            player.inventory = None

        # Player holding something + counter empty → place it down
        elif player.inventory is not None and self.item is None:
            self.item = player.inventory
            player.inventory = None

        # Player holding nothing + counter has something → pick it up
        elif player.inventory is None and self.item is not None:
            player.inventory = self.item
            self.item = None