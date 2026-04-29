from counter import Counter


CUT_RESULTS = {
    "tomato": "tomato_sliced",
    "lettuce": "lettuce_sliced",
}


class CuttingStation(Counter):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.station_type = "cutting_station"

    def cut_item(self, item):
        if item is not None and getattr(item, "name", None) in CUT_RESULTS:
            item.name = CUT_RESULTS[item.name]
            return True
        return False

    def interact(self, player):
        if self.cut_item(self.item):
            return

        super().interact(player)

    def draw(self, win, images, ingredient_images):
        img = images.get(self.station_type)
        if img:
            win.blit(img, (self.rect.x, self.rect.y))

        super().draw(win, {}, ingredient_images)
