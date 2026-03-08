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
        self.reset()

    def process_button(self, data, current_result, current_expression):
        data = self.button_codes.get(data, data)
        if data in self.button_codes: 
            data = self.button_codes[data]
        print(f"Button clicked with data = {repr(data)}")

        result = str(current_result)
        expression_display = str(current_expression)

        # ERRO ou AC
        if result == "Error" and data != "AC":
            result = "0"
            expression_display = ""
            self.reset()

        if data == "AC":
            self.reset()
            return {"result": "0", "expression": ""}

        # CE
        elif data == "CE":
            result = "0"
            self.new_operand = True

        # NÚMEROS
        elif data in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."):
            if result == "0" or self.new_operand:
                result = data
                self.new_operand = False
            else:
                result += data
            
            if self.in_function:
                self.expression = result

        # OPERADORES
        elif data in ("+", "-", "*", "/"):
            if self.expression == "" and self.new_operand and result != "0":
                self.expression = result + data
            elif self.expression == "":
                self.expression = result + data
            else:
                self.expression += result + data
            
            expression_display = self.expression
            self.new_operand = True

        # FUNÇÕES CIENTÍFICAS (TODAS iguais, modo expressão)
        elif data in ("sin", "cos", "tan", "log", "ln", "sqrt", "cbrt"):
            if self.new_operand and result != "0" and self.expression == "":
                self.expression = data + "(" + result
                result = data + "(" + result
            elif self.expression == "":
                self.expression = data + "("
                result = data + "("
            else:
                self.expression += data + "("
                result = data + "("
            
            self.in_function = True
            expression_display = self.expression
            self.new_operand = False

        # CONSTANTES
        elif data in ("pi", "e"):
            const = "pi" if data == "pi" else "E"
            if self.expression == "":
                self.expression = const
                result = const
            else:
                self.expression += const
                result = const
            
            expression_display = self.expression
            self.new_operand = True

        # POTÊNCIA
        elif data == "**":
            if self.expression == "":
                self.expression = result + "**"
            else:
                self.expression += result + "**"
            
            expression_display = self.expression
            result = "^"
            self.new_operand = False

        # FATORIAL
        elif data == "!":
            if self.expression == "":
                self.expression = "factorial(" + result + ")"
            else:
                self.expression += "factorial(" + result + ")"
            
            expression_display = self.expression
            result = "!"
            self.new_operand = True

        # IGUAL
        elif data == "=":
            final_expression = self.expression
            
            if self.in_function:
                if not final_expression.endswith(")"):
                    final_expression += ")"
            elif self.expression != "":
                final_expression += result
            
            expression_display = final_expression + "="
            print(f"Calculando: {final_expression}")
            
            try:
                sympy_expr = final_expression.replace("ln(", "log(")
                resultado = sp.sympify(sympy_expr).evalf()
                result = self.format_scientific_result(resultado)
                print(f"Resultado: {result}")
                
                self.reset(keep_result=resultado)
                self.expression = ""
                self.new_operand = True
                
            except Exception as e:
                result = "Error"
                print(f"Erro: {e}")
                self.reset()
                self.expression = ""
                self.new_operand = True

        return {
            "result": result,
            "expression": expression_display,
        }

    def format_scientific_result(self, num):
        try:
            n = float(num)
            if n.is_integer():
                return int(n)
            return f"{n:.8f}".rstrip("0").rstrip(".")
        except:
            return str(num)

    def reset(self, keep_result=None):
        self.operator = "+"
        self.new_operand = True
        self.expression = ""
        self.open_parens = 0
        self.in_function = False
        if keep_result is not None:
            self.operand1 = float(keep_result)
        else:
            self.operand1 = 0