import flet as ft


class DisplayComponent(ft.Column):
    def __init__(self):
        super().__init__(spacing=4)

        self.expression_display = ft.Text(
            value="",
            color=ft.Colors.WHITE70,
            size=16,
            text_align=ft.TextAlign.RIGHT,
        )

        self.result = ft.Text(
            value="0",
            color=ft.Colors.WHITE,
            size=24,
            text_align=ft.TextAlign.RIGHT,
        )

        self.controls = [
            ft.Row(
                controls=[self.expression_display],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Row(
                controls=[self.result],
                alignment=ft.MainAxisAlignment.END,
            ),
        ]

    def set_expression(self, value):
        self.expression_display.value = value

    def set_result(self, value):
        self.result.value = str(value)

    def get_expression(self):
        return self.expression_display.value

    def get_result(self):
        return self.result.value

    def clear(self):
        self.expression_display.value = ""
        self.result.value = "0"