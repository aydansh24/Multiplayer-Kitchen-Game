from ingredient import Ingredient
from station import Station

CRATE_ITEMS = {
    "tomato_crate": "tomato",
    "lettuce_crate": "lettuce",
    "meat_crate": "patty_raw",
    "bun_crate": "bun"
}

class Crate(Station):
    def __init__(self, x, y, crate_type):
        super().__init__(x, y)
        self.crate_type = crate_type

    def interact(self, player):
        if player.inventory is None:
            player.inventory = Ingredient(0, 0, CRATE_ITEMS[self.crate_type])

    def draw(self, win, images, ingredient_images):
        img = images.get(self.crate_type)
        if img:
            win.blit(img, (self.rect.x, self.rect.y))

        if self.item:
            item_img = ingredient_images.get(self.item.name)
            if item_img:
                x = self.rect.x + (self.rect.width - item_img.get_width()) // 2
                y = self.rect.y + (self.rect.height - item_img.get_height()) // 2
                win.blit(item_img, (x, y))