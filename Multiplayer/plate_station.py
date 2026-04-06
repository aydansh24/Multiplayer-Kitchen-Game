from station import Station
from player import Player
from plate import Plate

class PlateStation(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.station_type = "plate_station"

    def interact(self, player):

        # If player is holding a plate, add item to it
        if isinstance(player.inventory, Plate):
            if self.item:
                player.inventory.add_ingredient(self.item)
                self.item = None

        # If player is holding an ingredient, put it on a new plate
        elif player.inventory:
            self.item = Plate()
            self.item.add_ingredient(player.inventory)
            player.inventory = self.item
            self.item = None

        # Pick up plate if nothing is on the station
        elif self.item:
            player.inventory = Plate()

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