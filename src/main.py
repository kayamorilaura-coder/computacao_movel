#!uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "flet[all]",
#     "sympy",
# ]
# ///
import flet as ft
from views.calculator_view import CalculatorApp

def main(page: ft.Page):
    def handle_checked_item_click(e: ft.Event[ft.PopupMenuItem]):
        e.control.checked = not e.control.checked
        page.update()

    #ft.app(target=main, view=ft.MOBILE)

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("Calculadora"),
        center_title=False,
        bgcolor=ft.Colors.BLUE_GREY_400,
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.Icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(content="Histórico"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        content="Ver Histórico",
                        checked=False,
                        on_click=handle_checked_item_click,
                    ),
                ]
            ),
        ],
    )
    page.theme_mode = ft.ThemeMode.LIGHT
    #page.bgcolor.BLACK

    page.add(
        ft.SafeArea(
            expand=True,
            #bgcolor= ft.Colors.WHITE,
            content=ft.Container(
                   
                    alignment=ft.Alignment.CENTER,
                    #animate=ft.AnimationValue(true,30 ),
                    #dark_theme=ft.Theme,
                    #width=400,
                    content=CalculatorApp(),
                    #content=ft.Container(
                    #    content=CalculatorApp()
                    #)
                )
        )
    )
ft.run(main)