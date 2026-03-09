import flet as ft

from controllers.history_controller import HistoryController
from components.datatable import DataTableComponents

@ft.control
class HistoryView(ft.Column):
    def __init__(self):
        super().__init__()
        self.page = ft.Page
        self.controller = HistoryController()
        self.bgcolor = ft.Colors.WHITE
        self.expand = True  # ← movido para cima
        self._build_ui()

    def _build_ui(self):
        dados = self.controller.list()
        self.data_table = DataTableComponents(
            data=dados,
            on_delete=self._handle_delete,
            on_copy=self._handle_copy,
        )
        self.controls = [
            ft.Text("Histórico de operações", size=20, weight=ft.FontWeight.BOLD),
            self.data_table,
        ]

    def _handle_delete(self, id_):
        self.controller.delete(id_)
        dados = self.controller.list()
        self.data_table.data = dados
        self.data_table._build_table()
        self.update()

    import flet as ft

from controllers.history_controller import HistoryController
from components.datatable import DataTableComponents


@ft.control
class HistoryView(ft.Column):
    def __init__(self):
        super().__init__()
        self.clipboard = ft.Clipboard()
        self.controller = HistoryController()
        self.bgcolor = ft.Colors.WHITE
        self.expand = True

        self._build_ui()

    def _build_ui(self):
        dados = self.controller.list()

        self.data_table = DataTableComponents(
            data=dados,
            on_delete=self._handle_delete,
            on_copy=self._handle_copy,
        )

        self.controls = [
            ft.Text(
                "Histórico de operações",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            self.data_table,
        ]

    # -----------------------
    # DELETE
    # -----------------------
    def _handle_delete(self, id_):
        self.controller.delete(id_)

        dados = self.controller.list()
        self.data_table.data = dados
        self.data_table._build_table()

        self.update()

    # -----------------------
    # COPY
    # -----------------------
    def _handle_copy(self, string_copy):
        page = self.page   # ← forma correta em @ft.control

        texto = string_copy #f"ID: {row["id"]} |" #{row[1]} = {row[2]}"

        self.clipboard.set(string_copy)

        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Copiado:\n{string_copy}"),
            bgcolor=ft.Colors.GREEN_100,
        )

        page.snack_bar.open = True
        page.update()
