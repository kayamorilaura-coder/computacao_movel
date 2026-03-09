import flet as ft

from components.display import DisplayComponent
from components.keyboard import KeyboardComponent
from controllers.calculator_controller import CalculatorController


@ft.control
class CalculatorApp(ft.Container):
    def init(self):
        self.controller = CalculatorController()
        self.expand = True
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 16

        self.display = DisplayComponent()
        self.keyboard = KeyboardComponent(self.button_clicked)

        self.display.expand = 2
        self.keyboard.expand = 8

        self.content = ft.Column(
            expand=True,
            spacing=12,
            controls=[
                self.display,
                self.keyboard,
            ],
        )

    def button_clicked(self, e):
        data = e.control.content

        state = self.controller.process_button(
            data=data,
            current_result=self.display.get_result(),
            current_expression=self.display.get_expression(),
        )

        self.display.set_result(state["result"])
        self.display.set_expression(state["expression"])
        self.update()