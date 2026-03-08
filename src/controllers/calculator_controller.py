import sympy as sp
#arrumar o print

class CalculatorController:
    def __init__(self): #tradutores para o print
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
            "log": sp.log,  # ln natural
            "ln": lambda x: sp.log(x)/sp.log(10),  #log base 10 usando mudança de base  
        }

        self.reset()
        #self.history_controller = HistoryController() ainda não tenho na minha branch

    def process_button(self, data, current_result, current_expression):
        data = self.button_codes.get(data, data)
        if data in self.button_codes: 
            data = self.button_codes[data]
        print(f"Button clicked with data = {repr(data)}")

        result = str(current_result)
        expression_display = str(current_expression)

        if result == "Error" and data != "AC": 
            result = "0"
            expression_display = ""
            self.reset()

#funções de operações
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
            #try:
            #    x = float(result)
            #    x_rad = x * sp.pi / 180
            #    resultado = self.func[data](x_rad).evalf()
            #    result = str(self.format_scientific_result(resultado))
            #    self.new_operand = True
            #except Exception:
            #    result = "Error"
            func_name = data
            if self.expression == "":
                self.expression = func_name + "("
            else:
                self.expression += func_name + "("
            
            expression_display = self.expression
            result = func_name + "("
            self.open_parens += 1
            self.new_operand = False
            

        elif data == "log":
            #try:
            #    x = float(result)
            #    resultado = sp.log(x, 10).evalf()
            #    result = str(self.format_scientific_result(resultado))
            #    self.new_operand = True
            #except Exception:
            #    result = "Error"
            if self.expression == "":
                self.expression = "log("
            else:
                self.expression += "log("
            
            expression_display = self.expression
            result = "log("
            self.open_parens += 1
            self.new_operand = False


        elif data == "ln":
            #try:
            #    x = float(result)
            #    resultado = sp.log(x).evalf()
            #    result = str(self.format_scientific_result(resultado))
            #    self.new_operand = True
            #except Exception:
            #    result = "Error"
            if self.expression == "":
                self.expression = "ln("
            else:
                self.expression += "ln("
            
            expression_display = self.expression
            result = "ln("
            self.open_parens += 1
            self.new_operand = False

        elif data == "sqrt":
            #try:
            #    x = float(result)
            #    if x < 0:
            #        result = "Error"
            #    else:
            #        resultado = sp.sqrt(x).evalf()
            #        result = str(self.format_scientific_result(resultado))
            #        self.new_operand = True
            #except Exception:
            #    result = "Error"
            if self.expression == "":
                self.expression = "√"
            else:
                self.expression += "√"
            
            expression_display = self.expression
            result = "√"
            self.open_parens += 1
            self.new_operand = False


        elif data == "cbrt":
            #try:
            #    x = float(result)
            #    resultado = sp.cbrt(x).evalf()
            #except Exception:
            #    result = "Error"
            #try:
            #    x = float(result)
            #    resultado = sp.cbrt(x).evalf()
            #    result = str(self.format_scientific_result(resultado))
            #    self.new_operand = True
            #except Exception:
            #    result = "Error"
            if self.expression == "":
                self.expression = "∛"
            else:
                self.expression += "∛"
            
            expression_display = self.expression
            result = "∛"
            self.open_parens += 1
            self.new_operand = False
            

        elif data == "!":
            #try:
            #    x = float(result)
            #    if x < 0:
            #        resultado = -sp.factorial(abs(int(x))).evalf()
            #    else:
            #        resultado = sp.factorial(int(x)).evalf()
            #    result = str(self.format_scientific_result(resultado))
            #    self.new_operand = True
            #except Exception:
            #    result = "Error"
            if self.expression == "":
                self.expression = "(" + result + ")" + "!"
            else:
                self.expression += "(" + result + ")" + "!"
            
            expression_display = self.expression
            result = "!"
            self.new_operand = True


        elif data == "pi":
            #try:
            #    result = str(self.format_scientific_result(sp.pi.evalf()))
            #    self.new_operand = True
            #except Exception:
            #    result = "Error"
            const = "pi" #chamar do sympy
            if self.expression == "":
                self.expression = const
                result = const
            else:
                self.expression += const
                result = const
            
            expression_display = self.expression
            self.new_operand = True


        elif data == "e":
            #try:
            #    result = str(self.format_scientific_result(sp.E.evalf()))
            #    self.new_operand = True
            #except Exception:
            #    result = "Error"
            const = "E" #sympy usa E maiusculo para EULER
            if self.expression == "":
                self.expression = const
                result = const
            else:
                self.expression += const
                result = const
            
            expression_display = self.expression
            self.new_operand = True


        elif data == "**":
            try:
                x = float(result)
                resultado = sp.Pow(x, 2).evalf()
                result = str(self.format_scientific_result(resultado))
                self.new_operand = True
            except Exception:
                result = "Error"

        elif data == "()":

            # Fecha parênteses pendentes
            final_expression = self.expression + result
            final_expression += ")" * max(0, self.open_parens)
            
            expression_display = final_expression + "="
            print(f"Calculando: {final_expression}")
            
            try:
                # Substitui ln por log (SymPy usa log para natural)
                sympy_expr = final_expression.replace("ln(", "log(")
                
                resultado = sp.sympify(sympy_expr).evalf()
                result = self.format_scientific_result(resultado)
                print(f"Resultado: {result}")
                
                self.reset(keep_result=resultado)
                self.expression = str(resultado)  # Permite continuar calculando
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