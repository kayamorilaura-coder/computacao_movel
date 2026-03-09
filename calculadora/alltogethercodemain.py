from dataclasses import field
import flet as ft
import sympy as sp

# CLASSES 

@ft.control #classe base para os botões, com a propriedade expand para permitir que o botão "0" ocupe o dobro do espaço
class CalcButton(ft.Button):                                          
    expand: int = field(default_factory=lambda: 1) #


@ft.control 
class DigitButton(CalcButton):  #subclasse para os botões numéricos                                          
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE

@ft.control 
class OperatorButton(CalcButton): #subclasse para o = que vai ser o oficial mandachuva
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_300
    color: ft.Colors = ft.Colors.BLACK

@ft.control 
class ActionButton (CalcButton):  #subclasse para os otão e os operadores básicos (+, -, *, /)
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100                                   
    color: ft.Colors = ft.Colors.BLACK   

@ft.control 
class ScientificButton(CalcButton): #subclasse para os botões de funções científicas
    bgcolor = ft.Colors.BLUE_200                                          
    color = ft.Colors.BLACK


@ft.control
class CalculatorApp(ft.Container): #classe principal da calculadora, que herda de ft.Container para organizar os elementos visuais
    def __init__(self):
        super().__init__()
        self.reset()                                                            
        self.width = 450
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20, text_align= ft.TextAlign.RIGHT) #display para mostrar o resultado atual
        self.expression_display = ft.Text(value="", color=ft.Colors.WHITE, size=16, text_align= ft.TextAlign.RIGHT) #display para mostrar a expressão completa
        self.button_codes = {
            "√": "sqrt",    # Quando clica em √, trata como "sqrt"
            "∛": "cbrt",    #  # Quando clica em ∛ trata como "cbrt"
            "π": "pi",
            "×": "*",       
            "÷": "/", 
            "^": "**",        
        }

    #mapeamento das funções cientificas dentro da classe da calculadora
        self.func = {
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "log": sp.log,  # ln natural
            "ln": lambda x: sp.log(x)/sp.log(10),  #log base 10 usando mudança de base  
            }
    #mapeamento das colunas da calculadora    
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.expression_display, self.result],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        ActionButton(content="AC", on_click=self.button_clicked),
                        ActionButton(content="+/-", on_click=self.button_clicked),
                        ActionButton(content="%", on_click=self.button_clicked),
                        ActionButton(content="÷", on_click=self.button_clicked),
                        ActionButton(content="CE", on_click=self.button_clicked)
                    ]
                ),
                
                ft.Row(
                    controls=[
                        ScientificButton(content="sin", on_click=self.button_clicked),
                        ScientificButton(content="cos", on_click=self.button_clicked),
                        ScientificButton(content="tan", on_click=self.button_clicked),
                        ScientificButton(content="π", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ScientificButton(content="log", on_click=self.button_clicked),
                        ScientificButton(content="ln", on_click=self.button_clicked),
                        ScientificButton(content="^", on_click=self.button_clicked),
                        ScientificButton(content="√", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[ 
                        ScientificButton(content="()", on_click=self.button_clicked),   #IDEIA:
                        ScientificButton(content="e", on_click=self.button_clicked),    #colocar as expressões dentro do () vai ser inteligente e programado dependendo do começo ou fim
                        ScientificButton(content="∛", on_click=self.button_clicked),
                        ScientificButton(content="!", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.button_clicked),
                        DigitButton(content="8", on_click=self.button_clicked),
                        DigitButton(content="9", on_click=self.button_clicked),
                        ActionButton(content="×", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.button_clicked),
                        DigitButton(content="5", on_click=self.button_clicked),
                        DigitButton(content="6", on_click=self.button_clicked),
                        ActionButton(content="-", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.button_clicked),
                        DigitButton(content="2", on_click=self.button_clicked),
                        DigitButton(content="3", on_click=self.button_clicked),
                        ActionButton(content="+", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            content="0", expand=2, on_click=self.button_clicked
                        ),
                        DigitButton(content=".", on_click=self.button_clicked),
                        OperatorButton(content="=", on_click=self.button_clicked),
                    ]
                ),
            ]
        )
#operações
    def button_clicked(self, e):    #método lidar com os botões de ação
        data = e.control.content
        if data in self.button_codes: 
            data = self.button_codes[data]
        print(f"Button clicked with data = {repr(data)}")


        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

#Funções básicas que usam 2 ou mais operadores (+, -, *, /) e funções científicas (sin, cos, tan, log, ln) que usam 1 operador
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data
        
        elif data == "AC":
            self.result.value = "0"
            self.expression = ""  # ← Limpa expressão também!
            self.expression_display.value = ""  # ← Limpa display superior!
            self.reset()

        elif data == "CE":  # NOVO!
            self.result.value = "0"  # ← Só limpa display atual
            self.new_operand = True  # ← Próximo dígito limpa
            # NÃO limpa self.expression! Permite continuar expressão

        elif data in ("+", "-", "*", "/"):
            if self.expression == "":
                    self.expression = self.result.value + data
            else:
                self.expression += self.result.value + data
            self.expression_display.value = self.expression  # Nome correto!
            self.new_operand = True
                                                                                                        
        elif data == "=":
            self.expression += self.result.value #adiciona último número 
            self.expression_display.value = self.expression + "=" #mostra expressão completa com =
            
            try:
                resultado = sp.sympify(self.expression).evalf() # CALCULA TUDO!
                self.result.value = self.format_scientific_result(resultado)
                self.reset(keep_result=resultado) #reseta mas mantém resultado para continuar
            except Exception as e:
                self.result.value = "Error"
                print(f"Erro no cálculo: {e}")
                self.reset()
            self.expression = ""
            self.new_operand = True #limpa expressão para próximo cálculo


        elif data == "%":
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data == "+/-":
            #if float(self.result.value) > 0: "(" ")" não é visto como um numero
            try: 
                x = float(self.result.value) #tenta converter - se der erro, não é número simples
                if x > 0:
                    self.result.value = "-" + str(x)
                elif x < 0:
                    self.result.value = str(abs(x))
            except ValueError: #se não for número (tem "(" ou operadores), ignora ou mostra erro
                pass  #ou: self.result.value = "Error"


#Funções cientificas (sin, cos, tan, log, ln, pi, sqrt, cbrt, !, **) usando a biblioteca sympy para cálculos precisos e conversão de graus para RADIANOS
        elif data in ("sin", "cos", "tan", "log", "ln"): 
            try:
                x = float(self.result.value)
                x_rad = x * sp.pi / 180  # Converte para radianos 
                resultado = self.func[data](x_rad).evalf()  # Calcula usando a função mapeada     
            except Exception as e:
                self.result.value = "Error"
                print(f"Erro: {e}")
            func_name = data  
            if self.expression == "":
                self.expression = func_name + "("
            else:
                self.expression += func_name + "("
            # Atualiza display para mostrar que está dentro da função
            self.result.value = func_name + "("
            self.open_parens += 1  # Conta o parêntese aberto
            self.new_operand = False  # Próximo número entra dentro do ()



        elif data == "sqrt":
            try:
                x = float(self.result.value)
                if x < 0:
                    self.result.value = "Error"
                else: 
                    resultado = sp.sqrt(x).evalf() # Calcula a raiz quadrada usando sympy sqrt
                    self.result.value = self.format_scientific_result(resultado)
                    self.new_operand = True
            except:
                self.result.value = "Error"

        elif data == "cbrt":
            try:
                x = float(self.result.value)
                resultado = sp.cbrt(x).evalf() # Calcula a raiz cubica usando sympy sqrt
                self.result.value = self.format_scientific_result(resultado)
                self.new_operand = True
            except:
                self.result.value = "Error"

        elif data == "!":
            try:
                x = float(self.result.value)
                if x < 0: #interpretação: -(n!) 
                    resultado = -sp.factorial(abs(x)).evalf()
                else:
                    resultado = sp.factorial(x).evalf()
                self.result.value = self.format_scientific_result(resultado)
                self.new_operand = True
            except:
                self.result.value = "Error"

        elif data == "pi":
                resultado = str(sp.pi.evalf())
                self.result.value = self.format_scientific_result(resultado)
                self.new_operand = True

        elif data == "^":  
            try:
                x = float(self.result.value)
                resultado = sp.Pow(x, 2).evalf()  # Eleva ao quadrado usando sympy Pow
                self.result.value = self.format_scientific_result(resultado)
                self.new_operand = True
            except Exception as e:
                self.result.value = "Error"
                print(f"Erro: {e}")

        elif data == "()":
            if self.open_parens == 0:
                # Abre
                if self.result.value == "0" or self.new_operand:
                    self.result.value = "("
                else:
                    self.result.value += "("
                self.open_parens += 1
            else:
                # Fecha
                self.result.value += ")"
                self.open_parens -= 1
            self.new_operand = False



    def format_number(self, num): #formata numeros simples (inteiros e decimais)
        if isinstance(num, (int, float)):
            if float(num) % 1 == 0:
                return int(num)
            else:
                return num
        return num
    
    def format_scientific_result(self, num): #formata resultados cientificos para arrendar para 8 casas decimais e remover zeros à direita
        try: 
            n = float(num)
            if n.is_integer():
                return int(n) #se o resultado for inteiro, retorna como inteiro
            return f"{n:.8f}".rstrip('0').rstrip('.') #senão, limita a 8 casas decimais e remove zeros à direita
        except:
            return str(num) #se não for um número, retorna como string

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
            else:
                return self.format_number(operand1 / operand2)

    def reset(self, keep_result=False): #reseta a calculadora para o estado inicial, com a opção de manter o resultado atual
        self.operator = "+" #operador padrão para o próximo cálculo, para evitar erros se o usuário clicar em "=" sem escolher um operador
        self.new_operand = True 
        self.expression = ""    #string para construir a expressão completa, especialmente para funções científicas e parênteses
        self.open_parens= 0 #contador para controlar os parênteses abertos e fechados, garantindo que a expressão seja válida
        if  keep_result is not None:
            self.operand1 = float(keep_result)
        else: #Limpa tudo, função do AC
            self.operand1 = 0
        #self.add_to_history(self.expression, str(resultado)) #adiciona o cálculo ao histórico
        
def main(page: ft.Page):
    page.title = "Calc App"
    calc = CalculatorApp()
    page.add(calc)

    
ft.run(main)