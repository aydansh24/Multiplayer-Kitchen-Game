from plate import Plate
from station import Station

VALID_PLATE_INGREDIENTS = {"patty_cooked", "lettuce_sliced", "tomato_sliced", "bun"}

def is_platable(ingredient):
    return getattr(ingredient, "name", None) in VALID_PLATE_INGREDIENTS

class Counter(Station):
    def __init__(self, x, y, counter_type):
        super().__init__(x, y)
        self.counter_type = counter_type

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

    def draw(self, win, images, ingredient_images):
        img = images.get(self.counter_type)
        if img:
            win.blit(img, (self.rect.x, self.rect.y))

        if self.item:
            cx = self.rect.x + self.rect.width // 2
            cy = self.rect.y + self.rect.height // 2

            if isinstance(self.item, Plate):
                # Center the plate on the station
                plate_img = ingredient_images.get("plate")
                px = cx - (plate_img.get_width() // 2 if plate_img else 0)
                py = cy - (plate_img.get_height() // 2 if plate_img else 0) - 20
                self.item.draw(win, ingredient_images, px, py)
            else:
                item_img = ingredient_images.get(self.item.name)
                if item_img:
                    x = cx - item_img.get_width() // 2
                    y = cy - item_img.get_height() // 2 - 20
                    win.blit(item_img, (x, y))