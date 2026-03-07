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
from views.history_view import HistoryView


def main(page: ft.Page):
    page.title = "Calculadora"

    async def ir_calculadora(e):
        await page.push_route("/")

    async def ir_historico(e):
        await page.push_route("/history")

    def build_appbar():
        return ft.AppBar(
            title=ft.Text("Calculadora"),
            bgcolor=ft.Colors.BLUE_GREY_400,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Text("Calculadora"),
                            on_click=ir_calculadora,
                        ),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(
                            content=ft.Text("Histórico"),
                            on_click=ir_historico,
                        ),
                    ]
                )
            ],
        )

    def route_change(e):
        page.views.clear()

        page.views.append(
            ft.View(
                route="/",
                appbar=build_appbar(),
                controls=[
                    ft.SafeArea(
                        expand=True,
                        content=CalculatorApp(),
                    )
                ],
            )
        )

        if page.route == "/history":
            page.views.append(HistoryView())

        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        if e.view is not None:
            page.views.remove(e.view)
        if page.views:
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change(None)


ft.run(main)