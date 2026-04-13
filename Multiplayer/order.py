import random

ORDERS = [
    {"name": "Plain Burger", "ingredients": ["patty_cooked"]},
    {"name": "Lettuce Burger", "ingredients": ["patty_cooked", "lettuce"]},
    {"name": "Tomato Burger", "ingredients": ["patty_cooked", "tomato"]},
    {"name": "Full Burger", "ingredients": ["patty_cooked", "lettuce", "tomato"]},
]

class Order:
    def __init__(self):
        template = random.choice(ORDERS)
        self.name = template["name"]
        self.required = template["ingredients"][:]

    def matches(self, plate):
        plate_ingredients = sorted([i.name for i in plate.ingredients])
        return plate_ingredients == sorted(self.required)

    def __repr__(self):
        return f"Order({self.name}: {self.required})"