from plate import Plate
from station import Station

VALID_PLATE_INGREDIENTS = {"patty_cooked", "lettuce_sliced", "tomato_sliced", "bun"}

def is_platable(ingredient):
    return getattr(ingredient, "name", None) in VALID_PLATE_INGREDIENTS

class Counter(Station):
    def interact(self, player):
        # Player holding plate + counter has platable ingredient → add to plate
        if isinstance(player.inventory, Plate) and self.item is not None and not isinstance(self.item, Plate) and is_platable(self.item):
            player.inventory.add_ingredient(self.item)
            self.item = None

        # Player holding platable ingredient + counter has plate → add to plate
        elif player.inventory is not None and not isinstance(player.inventory, Plate) and isinstance(self.item, Plate) and is_platable(player.inventory):
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