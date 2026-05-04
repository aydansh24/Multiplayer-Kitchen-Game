BURGER_IMAGES = {
    frozenset(["patty_cooked", "bun"]):                                     "burger_plain",
    frozenset(["patty_cooked", "lettuce_sliced", "bun"]):                   "burger_lettuce",
    frozenset(["patty_cooked", "tomato_sliced", "bun"]):                    "burger_tomato",
    frozenset(["patty_cooked", "lettuce_sliced", "tomato_sliced", "bun"]):  "burger_full",
}

class Plate:
    def __init__(self):
        self.ingredients = []

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def is_empty(self):
        return len(self.ingredients) == 0

    def get_burger_image(self):
        names = frozenset(i.name for i in self.ingredients)
        return BURGER_IMAGES.get(names, None)

    def draw(self, win, imgs, x, y, offset_y=0):
        plate_img = imgs.get("plate")
        if plate_img:
            win.blit(plate_img, (x - plate_img.get_width() // 2, y))

        burger_img_name = self.get_burger_image()
        if burger_img_name:
            burger_img = imgs.get(burger_img_name)
            if burger_img:
                win.blit(burger_img, (x - burger_img.get_width() // 2, y - offset_y))
        else:
            for i, ingredient in enumerate(self.ingredients):
                img = imgs.get(ingredient.name)
                if img:
                    win.blit(img, (x - img.get_width() // 2, y - (i + 1) * 10 - offset_y))