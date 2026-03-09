from dataclasses import field
import flet as ft

# Responsabilidade :
# Criar estilos de botões
#
from dataclasses import field

import flet as ft


@ft.control #classe base para os botões, com a propriedade expand para permitir que o botão "0" ocupe o dobro do espaço
class CalcButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)


@ft.control #subclasse para os botões numéricos
class DigitButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE


@ft.control #subclasse para o = que vai ser o oficial do resultado
class OperatorButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_300
    color: ft.Colors = ft.Colors.BLACK


@ft.control #subclasse para os otão e os operadores básicos (+, -, *, /)
class ActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK


@ft.control #subclasse para os botões de funções científicas
class ScientificButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_200
    color: ft.Colors = ft.Colors.BLACK