# CalculatorController - VERSAO FINAL FUNCIONAL
import sympy as sp
from datetime import datetime

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
        # Mapeamento das funções científicas do SymPy
        self.func = {
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "log": sp.log,  # ln natural
            "ln": lambda x: sp.log(x)/sp.log(10),  # log base 10
        }
        
        self.reset()

    def reset(self, keep_result=None):
        #self.operator = "+" #operador pardrão para o próximo calculo, caso clique-se em "=" sem nada 
        self.new_operand = True
        self.expression = ""          # Expressao acumulada
        self.current_number = "0"     # Numero sendo digitado
        self.last_result = None
        self.last_expression = ""
        self.open_parens = 0 #contador para controlar os parenteses
        if keep_result is not None:
            self.operand1 = float(keep_result)
        else:
            self.operand1 = 0

    def process_button(self, data): #Mapeia os simbolos visuais
        original_data = data
        if data in self.button_codes:
            data = self.button_codes[data]
        
        print(f"Button clicked with data = {repr(data)}")

        # ERRO - Só permite AC
        if self.get_display() == "Error" and data != "AC":
            return {"result_display": "Error", "expression_display": self.expression}

        # AC - Limpa tudo
        if data == "AC":
            self.reset()
            return {"result_display": "0", "expression_display": ""}

        # CE  - limpa display atual
        elif data == "CE":
            self.current_number = "0"
            self.new_operand = True
            return {"result_display": "0", "expression_display": self.expression}

        # BACKSPACE - CORRIGIDO PARA APAGAR DA EXPRESSION TAMBEM
        #elif data in ("⌫", "Backspace"):


        # NUMEROS
        elif data in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."):
            if self.current_number == "0" or self.new_operand:
                if data == ".":
                    self.current_number = "0."
                else:
                    self.current_number = data
                self.new_operand = False
            else:
                if data == "." and "." in self.current_number:
                    pass
                else:
                    self.current_number += data
            
            return {"result_display": self.get_display(), "expression_display": self.expression}

        # OPERADORES
        elif data in ("+", "-", "*", "/"):
            if self.expression == "":
                self.expression = self.current_number + data
            else:
                if self.expression[-1] in "+-*/":
                    self.expression = self.expression[:-1] + data
                else:
                    self.expression += self.current_number + data
            
            self.current_number = "0"
            self.new_operand = True
            return {"result_display": data, "expression_display": self.expression}

        # FUNCOES CIENTIFICAS - COM CONVERSAO GRAUS PARA RADIANOS
        elif data in ("sin", "cos", "tan", "log", "ln", "sqrt", "cbrt"):
            # Se tem numero atual, adiciona ele primeiro
            if self.current_number != "0" and not self.new_operand:
                # Converte numero para radianos se for funcao trigonométrica
                if data in ("sin", "cos", "tan"):
                    # Converte: 45 graus -> 45 * pi / 180 radianos
                    arg = x * sp.pi / 180
                else:
                    arg = self.current_number
                
                if self.expression != "" and self.expression[-1] not in "+-*/(":
                    self.expression += "*" + data + "(" + arg
                else:
                    self.expression += data + "(" + arg
                self.current_number = "0"
            else:
                # So a funcao (espera numero depois)
                if self.expression != "" and self.expression[-1] not in "+-*/(":
                    self.expression += "*" + data + "("
                else:
                    self.expression += data + "("
            
            self.new_operand = False
            return {"result_display": data + "(", "expression_display": self.expression}

        # CONSTANTES
        elif data in ("pi", "e"):
            const = "pi" if data == "pi" else "E"
            
            if self.expression != "" and self.expression[-1] not in "+-*/(":
                self.expression += "*" + const
            else:
                self.expression += const
            
            self.current_number = const
            self.new_operand = True
            return {"result_display": original_data, "expression_display": self.expression}

        # POTENCIA
        elif data == "**":
            if self.expression == "":
                self.expression = self.current_number + "**"
            else:
                self.expression += self.current_number + "**"
            
            self.current_number = "0"
            self.new_operand = True
            return {"result_display": "^", "expression_display": self.expression}

        # FATORIAL
        elif data == "!":
            if self.expression == "":
                self.expression = "factorial(" + self.current_number + ")"
            else:
                self.expression += "factorial(" + self.current_number + ")"
            
            self.current_number = "0"
            self.new_operand = True
            return {"result_display": "!", "expression_display": self.expression}

        # PARENTSES - CORRIGIDO!
        elif data == "()":
            # Se expression vazia ou termina em operador/(, abre
            if self.expression == "" or self.expression[-1] in "+-*/(":
                self.expression += "("
                return {"result_display": "(", "expression_display": self.expression}
            else:
                # Senao, fecha
                self.expression += ")"
                return {"result_display": ")", "expression_display": self.expression}

        # +/-
        elif data == "+/-":
            try:
                x = float(self.current_number)
                if x > 0:
                    self.current_number = "-" + str(x)
                elif x < 0:
                    self.current_number = str(abs(x))
            except ValueError:
                if not self.current_number.startswith("-"):
                    self.current_number = "-" + self.current_number
                else:
                    self.current_number = self.current_number[1:]
            
            return {"result_display": self.get_display(), "expression_display": self.expression}

        # PORCENTAGEM
        elif data == "%":
            try:
                x = float(self.current_number)
                res = x / 100
                self.current_number = self.format_scientific_result(res)
                self.new_operand = True
            except:
                self.current_number = "Error"
            
            return {"result_display": self.get_display(), "expression_display": self.expression}

        # IGUAL
        elif data == "=":
            return self._calculate_result()

        return {"result_display": self.get_display(), "expression_display": self.expression}

    def get_display(self):
        """Retorna o que deve aparecer no display inferior"""
        if self.expression == "":
            return self.current_number
        # Se expression termina em ( ou operador, mostra numero atual
        if self.expression[-1] in "+-*/(":
            if self.current_number != "0" or self.new_operand:
                return self.expression + self.current_number
        return self.expression

    def _calculate_result(self):
        # Monta expressao final
        final_expression = self.expression
        
        # Adiciona numero atual se necessario
        if final_expression == "":
            final_expression = self.current_number
        elif final_expression[-1] in "+-*/(":
            final_expression += self.current_number
        
        # Fecha parenteses pendentes
        open_parens_parenss = final_expression.count("(")
        closes = final_expression.count(")")
        final_expression += ")" * (open_parenss - closes)
        
        print(f"Calculando: {final_expression}")
        
        try:
            sympy_expr = final_expression.replace("ln(", "log(")
            res = sp.sympify(sympy_expr).evalf()
            result = self.format_scientific_result(res)
            print(f"Resultado: {result}")
            
            self.last_expression = final_expression
            self.last_result = result
            
            self.reset(keep_result=res)
            self.current_number = result
            
            return {
                "result_display": result,
                "expression_display": final_expression + "="
            }
            
        except Exception as e:
            print(f"Erro no calculo: {e}")
            self.reset()
            return {
                "result_display": "Error",
                "expression_display": final_expression + "="
            }

    def format_scientific_result(self, num):
        """Formata resultado: inteiros sem decimal, decimais com 8 casas max"""
        try:
            n = float(num)
            if n.is_integer():
                return str(int(n))
            return f"{n:.8f}".rstrip("0").rstrip(".")
        except:
            return str(num)

    def get_history_entry(self):
        if self.last_expression and self.last_result:
            return {
                "expression": self.last_expression,
                "result": self.last_result,
                "timestamp": datetime.now().isoformat()
            }
        return None