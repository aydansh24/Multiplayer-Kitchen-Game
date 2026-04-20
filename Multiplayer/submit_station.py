from station import Station
from plate import Plate

class SubmitStation(Station):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.station_type = "submit_station"

    def interact(self, player):
        # Only accepts plates with ingredients
        if isinstance(player.inventory, Plate) and not player.inventory.is_empty():
            player.inventory = "submit"  # signal to server

    def draw(self, win, images, ingredient_images):
        img = images.get("submit_station")
        if img:
            win.blit(img, (self.rect.x, self.rect.y))