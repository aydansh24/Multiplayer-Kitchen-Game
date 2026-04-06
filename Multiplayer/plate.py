class Plate:
    def __init__(self):
        self.ingredients = []  # List of Ingredient objects

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def is_empty(self):
        return len(self.ingredients) == 0

    def __repr__(self):
        return f"Plate({[i.name for i in self.ingredients]})"