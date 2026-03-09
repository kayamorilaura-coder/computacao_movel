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
        
        # CORRECAO: Usa lambda para atrasar a referencia ao metodo
        # Isso resolve o problema de ordem (init roda antes do metodo existir)
        self.keyboard = KeyboardComponent(lambda e: self.on_button_click(e))

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

    def on_button_click(self, e):
        """Processa clique do botao via Controller"""
        data = e.control.content

        # Controller stateful - so passa data
        state = self.controller.process_button(data)

        # Atualiza displays com retorno correto
        self.display.set_result(state["result_display"])
        self.display.set_expression(state["expression_display"])
        
        # Salva historico se for "="
        if data == "=" and state["result_display"] != "Error":
            entry = self.controller.get_history_entry()
            if entry:
                print(f"Historico: {entry}")
        
        self.update()