from easy_shopping.calculator import Calculator
from easy_shopping.shopping import ShoppingCart


def main():
    calc = Calculator()
    #split the calculations into the class.method style
    calculations = [
        ("1. 7 + 5", calc.add(7, 5)),
        ("2. 34 - 21", calc.subtract(34, 21)),
        ("3. 54 * 2", calc.multiply(54, 2)),
        ("4. 144 / 2", calc.divide(144, 2)),
        ("5. 45 / 0", calc.divide(45, 0))
    ]
    #iterate over the calculations array to calc each calculation
    for calcs, result in calculations:
        print(calcs + " = " + str(result))


    cart = ShoppingCart()

    #add items
    cart.add_item("Cookie")
    cart.add_item("Fruit Salad")
    cart.add_item("Juice")
    cart.add_item("Cookie")

    #iterate over the cart items and return their respective quanitities
    print("Your cart contains:")
    for item, quantity in cart.items.items():
        print(f"{item}: {quantity}")
    print(f"Total quantity in the cart: {cart.calc_quantity()}")
    
    #remove items
    cart.remove_item("Cookie")
    cart.remove_item("Fruit Salad")

    #iterate over the cart items and return their respective quanitities
    print("Your cart contains:")
    for item, quantity in cart.items.items():
        print(f"{item}: {quantity}")
    print(f"Total quantity in the cart: {cart.calc_quantity()}")

    


if __name__ == "__main__":
    main()