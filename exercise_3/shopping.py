class ShoppingCart:

    def __init__(self):
        self.items = {}

    def add_item(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            print("Hi")
            self.items[item] = 1

    

    def remove_item(self, item):
        if item in self.items:
            self.items[item] -= 1
            if self.items[item] <= 0:
                del self.items[item]
            else:
                return "there are already no more of these items in your cart"
        else:
            return "this item has never been put into the cart"

    
    def calc_quantity(self):
        return sum(self.items.values())