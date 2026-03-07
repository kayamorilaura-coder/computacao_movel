from dataclasses import field
import flet as ft

# Responsabilidade :
# Criar estilos de botões
#
from dataclasses import field

import flet as ft


@ft.control
class CalcButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)


@ft.control
class DigitButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class OperatorButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_300
    color: ft.Colors = ft.Colors.BLACK


@ft.control
class ActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK


@ft.control
class ScientificButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_200
    color: ft.Colors = ft.Colors.BLACK