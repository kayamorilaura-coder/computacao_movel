import flet as ft

from components.buttons import (
    ActionButton,
    DigitButton,
    OperatorButton,
    ScientificButton,
)


class KeyboardComponent(ft.Column):
    def __init__(self, on_click):
        super().__init__(expand=True, spacing=8)

        self.controls = [
            ft.Row(
                expand=True,
                spacing=8,
                controls=[
                    ActionButton(content="AC", on_click=on_click),
                    ActionButton(content="+/-", on_click=on_click),
                    ActionButton(content="%", on_click=on_click),
                    ActionButton(content="÷", on_click=on_click),
                    ActionButton(content="CE", on_click=on_click),
                ],
            ),
            ft.Row(
                expand=True,
                spacing=8,
                controls=[
                    ScientificButton(content="sin", on_click=on_click),
                    ScientificButton(content="cos", on_click=on_click),
                    ScientificButton(content="tan", on_click=on_click),
                    ScientificButton(content="π", on_click=on_click),
                ],
            ),
            ft.Row(
                expand=True,
                spacing=8,
                controls=[
                    ScientificButton(content="log", on_click=on_click),
                    ScientificButton(content="ln", on_click=on_click),
                    ScientificButton(content="^", on_click=on_click),
                    ScientificButton(content="√", on_click=on_click),
                ],
            ),
            ft.Row(
                expand=True,
                spacing=8,
                controls=[
                    ScientificButton(content="()", on_click=on_click),
                    ScientificButton(content="e", on_click=on_click),
                    ScientificButton(content="∛", on_click=on_click),
                    ScientificButton(content="!", on_click=on_click),
                ],
            ),
            ft.Row(
                expand=True,
                spacing=8,
                controls=[
                    DigitButton(content="7", on_click=on_click),
                    DigitButton(content="8", on_click=on_click),
                    DigitButton(content="9", on_click=on_click),
                    ActionButton(content="×", on_click=on_click),
                ],
            ),
            ft.Row(
                expand=True,
                spacing=8,
                controls=[
                    DigitButton(content="4", on_click=on_click),
                    DigitButton(content="5", on_click=on_click),
                    DigitButton(content="6", on_click=on_click),
                    ActionButton(content="-", on_click=on_click),
                ],
            ),
            ft.Row(
                expand=True,
                spacing=8,
                controls=[
                    DigitButton(content="1", on_click=on_click),
                    DigitButton(content="2", on_click=on_click),
                    DigitButton(content="3", on_click=on_click),
                    ActionButton(content="+", on_click=on_click),
                ],
            ),
            ft.Row(
                expand=True,
                spacing=8,
                controls=[
                    DigitButton(content="0", expand=2, on_click=on_click),
                    DigitButton(content=".", on_click=on_click),
                    OperatorButton(content="=", on_click=on_click),
                ],
            ),
        ]