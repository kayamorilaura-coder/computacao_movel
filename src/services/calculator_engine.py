from sympy import sympify

class CalculatorEngine:
    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(expression):
        try:
            result = sympify(expression)
            return float(result)
        except:
            return "Error"
        
    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True
    
    
