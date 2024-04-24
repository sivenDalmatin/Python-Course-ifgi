class ShoppingCart:
    """class which represents a shopping cart,
     Includes methods for adding items, removing items and calculate the amount
     of total items in the shopping cart"""
    

    def __init__(self):
        #initalize an empty shopping cart
        self.items = {}


    def add_item(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1


    def remove_item(self, item):
        #item has to be in cart to be removable
        if item in self.items:
            self.items[item] -= 1
            #if its the last item not only the amount gets decreased, but it gets deleted
            if self.items[item] <= 0:
                del self.items[item]
        else:
            return "this item is not in your cart"
        
    
    def calc_quantity(self):
        return sum(self.items.values())