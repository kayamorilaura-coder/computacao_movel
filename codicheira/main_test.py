#!uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "flet[all]",
#     "sympy",
# ]
# ///
import flet as ft
def main(page: ft.Page):

    ft.PageView(
    controls=[
        ft.Container(bgcolor="red"),
        ft.Container(bgcolor="blue"),
        ft.Container(bgcolor="green"),
    ]
)