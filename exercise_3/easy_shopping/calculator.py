class Calculator:
    """class for performing mathematical operations, like + , - , * and /"""


    #addition
    def add(self, a, b):
        return a + b
    
    
    #subtraction
    def subtract(self, a, b):
        return a - b
    
    
    #multiplication
    def multiply(self, a, b):
        return a * b
    
    
    #division
    def divide(self, a, b):
        if b == 0:
            return "division by 0 is not allowed"
        return a / b