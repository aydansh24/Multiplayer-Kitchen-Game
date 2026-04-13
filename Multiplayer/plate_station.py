from station import Station
from player import Player
from plate import Plate

class PlateStation(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.station_type = "plate_station"

    def interact(self, player):
        # Player holds a plate → put it down
        if isinstance(player.inventory, Plate) and self.item is None:
            self.item = player.inventory
            player.inventory = None

        # Player has nothing and station has a plate → pick it up
        elif player.inventory is None and self.item is not None:
            player.inventory = self.item
            self.item = None

        # Player has nothing and station is empty → give fresh plate
        elif player.inventory is None and self.item is None:
            player.inventory = Plate()

        # Player holds an ingredient → wrap in new plate
        elif player.inventory is not None and self.item is None:
            new_plate = Plate()
            new_plate.add_ingredient(player.inventory)
            player.inventory = new_plate

    def draw(self, win, images, ingredient_images):
        img = images.get(self.station_type)  # uses the key "plate"
        if img:
            win.blit(img, (self.rect.x, self.rect.y))

        # If station holds a plate, draw it
        if self.item:
            item_img = ingredient_images.get("plate")
            if item_img:
                x = self.rect.x + (self.rect.width - item_img.get_width()) // 2
                y = self.rect.y + (self.rect.height - item_img.get_height()) // 2
                win.blit(item_img, (x, y))