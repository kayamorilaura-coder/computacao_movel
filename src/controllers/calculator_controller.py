from controllers.history_controller import HistoryController

import sympy as sp


class CalculatorController:
    def __init__(self):
        self.button_codes = {
            "√": "sqrt",
            "∛": "cbrt",
            "π": "pi",
            "×": "*",
            "÷": "/",
            "^": "**",
        }

        self.func = {
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
        }

        self.reset()
        self.history_controller = HistoryController()

    def process_button(self, data, current_result, current_expression):
        data = self.button_codes.get(data, data)

        result = str(current_result)
        expression_display = str(current_expression)

        if result == "Error" and data != "AC":
            result = "0"
            expression_display = ""
            self.reset()

        if data == "AC":
            self.reset()
            return {
                "result": "0",
                "expression": "",
            }

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if result == "0" or self.new_operand:
                result = data
                self.new_operand = False
            else:
                result = result + data

        elif data == "CE":
            result = "0"
            self.new_operand = True

        elif data in ("+", "-", "*", "/"):
            if self.expression == "":
                self.expression = result + data
            else:
                self.expression += result + data

            expression_display = self.expression
            self.new_operand = True

        elif data == "=":
            final_expression = self.expression + result if self.expression else result
            expression_display = final_expression + "="

            try:
                resultado = sp.sympify(final_expression).evalf()
                result = str(self.format_scientific_result(resultado))
                print(f'Resultado da conta: {resultado} e expressão: {expression_display}')
                self.history_controller.save(resultado, result)
                self.reset(keep_result=resultado)
            except Exception:
                result = "Error"
                self.reset()

            self.expression = ""
            self.new_operand = True

        elif data == "%":
            try:
                result = str(self.format_scientific_result(float(result) / 100))
            except Exception:
                result = "Error"
            self.reset()

        elif data == "+/-":
            try:
                x = float(result)
                if x > 0:
                    result = "-" + str(self.format_scientific_result(x))
                elif x < 0:
                    result = str(self.format_scientific_result(abs(x)))
            except ValueError:
                pass

        elif data in ("sin", "cos", "tan"):
            try:
                x = float(result)
                x_rad = x * sp.pi / 180
                resultado = self.func[data](x_rad).evalf()
                result = str(self.format_scientific_result(resultado))
                self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "log":
            try:
                x = float(result)
                resultado = sp.log(x, 10).evalf()
                result = str(self.format_scientific_result(resultado))
                self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "ln":
            try:
                x = float(result)
                resultado = sp.log(x).evalf()
                result = str(self.format_scientific_result(resultado))
                self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "sqrt":
            try:
                x = float(result)
                if x < 0:
                    result = "Error"
                else:
                    resultado = sp.sqrt(x).evalf()
                    result = str(self.format_scientific_result(resultado))
                    self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "cbrt":
            try:
                x = float(result)
                resultado = sp.cbrt(x).evalf()
                result = str(self.format_scientific_result(resultado))
                self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "!":
            try:
                x = float(result)
                if x < 0:
                    resultado = -sp.factorial(abs(int(x))).evalf()
                else:
                    resultado = sp.factorial(int(x)).evalf()
                result = str(self.format_scientific_result(resultado))
                self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "pi":
            try:
                result = str(self.format_scientific_result(sp.pi.evalf()))
                self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "e":
            try:
                result = str(self.format_scientific_result(sp.E.evalf()))
                self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "**":
            try:
                x = float(result)
                resultado = sp.Pow(x, 2).evalf()
                result = str(self.format_scientific_result(resultado))
                self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "()":
            if self.open_parens == 0:
                if result == "0" or self.new_operand:
                    result = "("
                else:
                    result += "("
                self.open_parens += 1
            else:
                result += ")"
                self.open_parens -= 1
            self.new_operand = False

        return {
            "result": result,
            "expression": expression_display,
        }

    def format_number(self, num):
        if isinstance(num, (int, float)):
            if float(num) % 1 == 0:
                return int(num)
            return num
        return num

    def format_scientific_result(self, num):
        try:
            n = float(num)
            if n.is_integer():
                return int(n)
            return f"{n:.8f}".rstrip("0").rstrip(".")
        except Exception:
            return str(num)

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "*":
            return self.format_number(operand1 * operand2)

        elif operator == "/":
            if operand2 == 0:
                return "Error"
            return self.format_number(operand1 / operand2)

    def reset(self, keep_result=None):
        self.operator = "+"
        self.new_operand = True
        self.expression = ""
        self.open_parens = 0

        if keep_result is not None:
            self.operand1 = float(keep_result)
        else:
            self.operand1 = 0