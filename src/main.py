#!uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "flet[all]",
#     "sympy",
#     "duckdb"
# ]
# ///

import flet as ft

from views.calculator_view import CalculatorApp
from views.history_view import HistoryView


def main(page: ft.Page):
    page.add(ft.Image(src=f"/images/loading-animation.gif"))
    page.title = "Calculadora" # Por defalt está na calculadora
    page.window_icon = "assets/favicon.png"
    page.theme_mode = ft.ThemeMode.LIGHT 
    page.bgcolor = ft.Colors.WHITE
    def ir_historico(e):
        page.go("/history")

    def ir_calculadora(e):
        page.go("/")
        # ------------------------------------------------------------------
    # Função que devover a App bar visto que o flet irá 
    # reconstruir toda a página
    #-------------------------------------------------------------------
    
    def build_appbar(): 
        return ft.AppBar(
            title=ft.Text("Calculadora"),
            #bgcolor=ft.Colors.BLUE_GREY_400,
            actions=[
                ft.IconButton(ft.Icons.HISTORY, on_click=ir_historico),
            ],
        )
    
    def history_appbar():
        return ft.AppBar(
            title=ft.Text("Histórico"),
            #bgcolor=ft.Colors.BLUE_GREY_400,
            actions=[
                ft.IconButton(ft.Icons.CALCULATE, on_click=ir_calculadora),
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
            page.views.append(
                ft.View(
                    route="/history",
                    appbar=history_appbar(),
                    controls=[
                        ft.SafeArea(
                            expand=True,
                            content=HistoryView(),
                        )
                    ],
            ))

        page.update()
        

    async def view_pop(e: ft.ViewPopEvent):
        if e.view is not None:
            page.views.remove(e.view)
        if page.views:
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change(None)


ft.run(main, assets_dir="assets")