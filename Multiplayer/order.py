import random

ORDERS = [
    {"name": "Plain Burger", "ingredients": ["bun", "patty_cooked"]},
    {"name": "Lettuce Burger", "ingredients": ["bun", "patty_cooked", "lettuce_sliced"]},
    {"name": "Tomato Burger", "ingredients": ["bun", "patty_cooked", "tomato_sliced"]},
    {"name": "Full Burger", "ingredients": ["bun", "patty_cooked", "lettuce_sliced", "tomato_sliced"]},
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
