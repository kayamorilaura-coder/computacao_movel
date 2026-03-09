# CalculatorController - VERSAO MVC & stateful
from controllers.history_controller import HistoryController
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

        # Mantido por compatibilidade
        self.func = {
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "log": sp.log,
            "ln": lambda x: sp.log(x) / sp.log(10),
        }

        self.reset()
        self.history_controller = HistoryController()

    def reset(self, keep_result=None):
        self.new_operand = True
        self.expression = ""
        self.current_number = "0"
        self.last_result = None
        self.last_expression = ""
        self.open_parens = 0

        if keep_result is not None:
            self.operand1 = float(keep_result)
        else:
            self.operand1 = 0

    def process_button(self, data):
        original_data = data
        if data in self.button_codes:
            data = self.button_codes[data]

        print(f"Button clicked with data = {repr(data)}")

        if self.get_display() == "Error" and data != "AC":
            return {"result_display": "Error", "expression_display": self.expression}

        # AC
        if data == "AC":
            self.reset()
            return {"result_display": "0", "expression_display": ""}

        # CE
        elif data == "CE":
            self.current_number = "0"
            self.new_operand = True
            return {"result_display": "0", "expression_display": self.expression}

        # NUMEROS
        elif data in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."):
            if self.new_operand:
                self.current_number = "0." if data == "." else data
                self.new_operand = False
            else:
                if data == ".":
                    if "." not in self.current_number:
                        if self.current_number in ("", "-"):
                            self.current_number += "0."
                        else:
                            self.current_number += "."
                else:
                    if self.current_number == "0":
                        self.current_number = data
                    elif self.current_number == "-0":
                        self.current_number = "-" + data
                    else:
                        self.current_number += data

            return {
                "result_display": self.get_display(),
                "expression_display": self.expression,
            }

        # OPERADORES
        elif data in ("+", "-", "*", "/"):
            if not self.new_operand:
                self._commit_current_number()

            if self.expression == "":
                self.expression = self.current_number if self.current_number != "0" else "0"

            if self._ends_with_operator(self.expression):
                self.expression = self.expression[:-1] + data
            elif self.expression.endswith("("):
                if data == "-":
                    self.expression += "0-"
                else:
                    self.expression += "0" + data
            else:
                self.expression += data

            self.current_number = "0"
            self.new_operand = True
            return {"result_display": data, "expression_display": self.expression}

        # FUNCOES CIENTIFICAS
        elif data in ("sin", "cos", "tan", "log", "ln", "sqrt", "cbrt"):
            if not self.new_operand and self.current_number not in ("", "0", "-0"):
                # Envolve o número actual na função
                func_expr = f"{data}({self.current_number})"
                self._append_value_token(func_expr)
                self.current_number = "0"
                self.new_operand = True
                return {
                    "result_display": self.get_display(),
                    "expression_display": self.expression,
                }

            # Só abre a função e espera o valor
            self._append_open_function(data)
            self.current_number = "0"
            self.new_operand = True
            return {
                "result_display": f"{data}(",
                "expression_display": self.expression,
            }

        # CONSTANTES
        elif data in ("pi", "e"):
            const = "pi" if data == "pi" else "E"
            self._append_value_token(const)
            self.current_number = "0"
            self.new_operand = True
            return {
                "result_display": original_data,
                "expression_display": self.expression,
            }

        # POTENCIA
        elif data == "**":
            if not self.new_operand:
                self._commit_current_number()
            elif self.expression == "":
                self.expression = self.current_number

            if self.expression == "":
                self.expression = "0**"
            elif self._ends_with_operator(self.expression):
                self.expression = self.expression[:-1] + "**"
            elif self.expression.endswith("("):
                self.expression += "0**"
            else:
                self.expression += "**"

            self.current_number = "0"
            self.new_operand = True
            return {"result_display": "^", "expression_display": self.expression}

        # FATORIAL
        elif data == "!":
            if not self.new_operand and self.current_number not in ("", "-", "-0"):
                fact_expr = f"factorial({self.current_number})"
                self._append_value_token(fact_expr)
                self.current_number = "0"
                self.new_operand = True
            elif self.expression == "":
                self.expression = "factorial(0)"
            elif self.expression.endswith("("):
                self.expression += "factorial(0)"
            else:
                # Se não há número em edição, evita quebrar a expressão
                self.expression = f"factorial({self._build_final_expression()})"
                self.current_number = "0"
                self.new_operand = True

            return {"result_display": "!", "expression_display": self.expression}

        # PARENTESES
        elif data == "()":
            return self._handle_parentheses()

        # +/-
        elif data == "+/-":
            if self.new_operand:
                self.current_number = "-0"
                self.new_operand = False
            else:
                if self.current_number.startswith("-"):
                    self.current_number = self.current_number[1:]
                    if self.current_number == "":
                        self.current_number = "0"
                        self.new_operand = True
                else:
                    self.current_number = "-" + self.current_number

            return {
                "result_display": self.get_display(),
                "expression_display": self.expression,
            }

        # PORCENTAGEM
        elif data == "%":
            try:
                value = self._safe_float(self.current_number)
                res = value / 100
                self.current_number = self.format_scientific_result(res)
                self.new_operand = True
            except Exception:
                self.current_number = "Error"

            return {
                "result_display": self.get_display(),
                "expression_display": self.expression,
            }

        # IGUAL
        elif data == "=":
            return self._calculate_result()

        return {"result_display": self.get_display(), "expression_display": self.expression}

    def get_display(self):
        if self.expression == "":
            return self.current_number

        preview = self._build_preview_expression()
        return preview if preview else self.expression

    def _calculate_result(self):
        final_expression = self._build_final_expression()

        if final_expression == "":
            final_expression = "0"

        # Fecha parênteses pendentes
        opens = final_expression.count("(")
        closes = final_expression.count(")")
        if opens > closes:
            final_expression += ")" * (opens - closes)

        print(f"Calculando: {final_expression}")

        try:
            sympy_expr, local_dict = self._prepare_expression_for_sympy(final_expression)
            res = sp.sympify(sympy_expr, locals=local_dict).evalf()
            result = self.format_scientific_result(res)

            print(f"Resultado: {result}")

            self.last_expression = final_expression
            self.last_result = result

            self.history_controller.save(final_expression, result)
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
        try:
            n = float(num)
            if n.is_integer():
                return str(int(n))
            return f"{n:.8f}".rstrip("0").rstrip(".")
        except Exception:
            return str(num)

    def get_history_entry(self):
        if self.last_expression and self.last_result:
            return {
                "expression": self.last_expression,
                "result": self.last_result,
                "timestamp": datetime.now().isoformat()
            }
        return None

    # =========================
    # Helpers internos
    # =========================

    def _safe_float(self, value):
        if value in ("", "-", "-0"):
            return 0.0
        return float(value)

    def _ends_with_operator(self, expr):
        return bool(expr) and expr[-1] in "+-*/"

    def _ends_with_power(self, expr):
        return expr.endswith("**")

    def _ends_with_open_paren(self, expr):
        return bool(expr) and expr[-1] == "("

    def _ends_with_value(self, expr):
        if not expr:
            return False
        return expr[-1].isalnum() or expr[-1] == ")" or expr[-1] == "."

    def _needs_implicit_multiplication(self):
        return self._ends_with_value(self.expression)

    def _append_value_token(self, token):
        if self.expression == "":
            self.expression = token
        elif self._needs_implicit_multiplication():
            self.expression += "*" + token
        elif self._ends_with_operator(self.expression) or self._ends_with_open_paren(self.expression):
            self.expression += token
        else:
            self.expression += token

    def _append_open_function(self, func_name):
        token = f"{func_name}("
        if self.expression == "":
            self.expression = token
        elif self._needs_implicit_multiplication():
            self.expression += "*" + token
        elif self._ends_with_operator(self.expression) or self._ends_with_open_paren(self.expression):
            self.expression += token
        else:
            self.expression += token

        self.open_parens += 1

    def _commit_current_number(self):
        if self.new_operand:
            return

        number = self.current_number
        if number in ("", "-"):
            number = "0"
        elif number == "-0":
            number = "0"

        self._append_value_token(number)
        self.current_number = "0"
        self.new_operand = True

    def _build_preview_expression(self):
        if self.expression == "":
            return self.current_number

        if not self.new_operand:
            current = self.current_number
            if current in ("",):
                current = "0"

            if self._ends_with_operator(self.expression) or self._ends_with_open_paren(self.expression):
                return self.expression + current

            if self._ends_with_value(self.expression):
                return self.expression + "*" + current

        return self.expression

    def _build_final_expression(self):
        final_expression = self.expression

        if not self.new_operand:
            current = self.current_number
            if current in ("", "-"):
                current = "0"
            elif current == "-0":
                current = "0"

            if final_expression == "":
                final_expression = current
            elif self._ends_with_operator(final_expression) or self._ends_with_open_paren(final_expression):
                final_expression += current
            elif self._ends_with_value(final_expression):
                final_expression += "*" + current

        elif final_expression == "":
            final_expression = self.current_number

        return final_expression

    def _handle_parentheses(self):
        # Caso 1: há número em edição
        if not self.new_operand:
            if self.open_parens > 0:
                self._commit_current_number()
                self.expression += ")"
                self.open_parens -= 1
                return {"result_display": ")", "expression_display": self.expression}
            else:
                self._commit_current_number()
                if self.expression == "":
                    self.expression = "("
                else:
                    self.expression += "*("
                self.open_parens += 1
                return {"result_display": "(", "expression_display": self.expression}

        # Caso 2: expressão vazia ou termina em operador/( -> abre
        if self.expression == "" or self._ends_with_operator(self.expression) or self._ends_with_open_paren(self.expression):
            self.expression += "("
            self.open_parens += 1
            return {"result_display": "(", "expression_display": self.expression}

        # Caso 3: termina em valor ou ) -> fecha se houver aberto, senão abre com multiplicação implícita
        if self._ends_with_value(self.expression):
            if self.open_parens > 0:
                self.expression += ")"
                self.open_parens -= 1
                return {"result_display": ")", "expression_display": self.expression}
            else:
                self.expression += "*("
                self.open_parens += 1
                return {"result_display": "(", "expression_display": self.expression}

        # fallback
        self.expression += "("
        self.open_parens += 1
        return {"result_display": "(", "expression_display": self.expression}

    def _prepare_expression_for_sympy(self, expression):
        expr = expression.strip()

        # Preserva "ln(" antes de converter "log("
        expr = expr.replace("ln(", "NATLOG(")
        expr = expr.replace("log(", "LOG10(")
        expr = expr.replace("NATLOG(", "log(")

        local_dict = {
            "pi": sp.pi,
            "E": sp.E,
            "sqrt": sp.sqrt,
            "factorial": sp.factorial,
            "cbrt": lambda x: x ** sp.Rational(1, 3),
            "sin": lambda x: sp.sin(x * sp.pi / 180),
            "cos": lambda x: sp.cos(x * sp.pi / 180),
            "tan": lambda x: sp.tan(x * sp.pi / 180),
            "LOG10": lambda x: sp.log(x, 10),
            "log": sp.log,
        }

        return expr, local_dict