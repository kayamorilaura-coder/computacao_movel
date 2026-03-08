import flet as ft

from controllers.history_controller import HistoryController
from components.datatable import DataTableComponents


@ft.control
class HistoryView(ft.Column):
    def __init__(self):
        super().__init__()
        self.controller = HistoryController()
        self.bgcolor = ft.Colors.WHITE
        self._build_ui()

    def _build_ui(self):
        dados = self.controller.list()
        self.data_table = DataTableComponents(data=dados)

        self.controls = [
            
            ft.Text("Histórico de operações", size=20, weight=ft.FontWeight.BOLD),
            self.data_table,
        ]
