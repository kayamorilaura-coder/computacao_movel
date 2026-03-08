import flet as ft


@ft.control
class DataTableComponents(ft.Column):
    def __init__(self, data=None):
        super().__init__()
        self.data = data or []
        self._build_table()
        self.bgcolor = ft.Colors.WHITE

    def _build_table(self):
        rows = []
        for row in self.data:
            id_, expression, result, created_at = row
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id_))),
                        ft.DataCell(ft.Text(str(expression))),
                        ft.DataCell(ft.Text(str(result))),
                        ft.DataCell(ft.Text(str(created_at))),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Apagar",
                                # on_click=... (você pode ligar depois)
                            )
                        ),
                    ]
                )
            )

        self.controls = [
            ft.DataTable(
                
                columns=[
                    ft.DataColumn(label=ft.Text("ID")),
                    ft.DataColumn(label=ft.Text("Expressão")),
                    ft.DataColumn(label=ft.Text("Resultado")),
                    ft.DataColumn(label=ft.Text("Criado em")),
                    ft.DataColumn(label=ft.Text("Ação")),
                ],
                rows=rows,
                expand=True,
            )
        ]
