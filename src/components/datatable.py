import flet as ft

@ft.control
class DataTableComponents(ft.Column):
    def __init__(self, data=None, on_delete=None, on_copy=None):
        super().__init__()
        self.data = data or []
        self._build_table()
        self.on_delete = on_delete
        self.on_copy = on_copy

    def _build_table(self):
        rows = []
        for row in self.data:
            id_, expression, result, created_at = row
            rows.append(
                ft.DataRow(
                    #on_click=lambda e: self.on_copy(row),
                    cells=[
                        ft.DataCell(ft.Text(str(id_))),
                        ft.DataCell(ft.Text(str(expression))),
                        ft.DataCell(ft.Text(str(result))),
                        ft.DataCell(ft.Text(str(created_at))),
                        ft.DataCell(  # ← só 1 célula para as ações
                            ft.Row(  # ← junta os 2 botões numa Row
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Apagar",
                                        on_click=lambda e, _id=id_: self.on_delete(_id)
                                    ),
                                    ft.IconButton(
                                    icon=ft.Icons.CONTENT_COPY,  # ← ícone de cópia
                                    tooltip="Copiar linha",
                                    on_click=lambda e, _id=id_: self.on_copy(f'Id: {id_} | Expressão: {expression} | Resultado: {result} | Criado em: {created_at}')
                                ),
                                ]
                            )
                        ),
                    ]
                )
            )

        table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Expressão")),
                ft.DataColumn(label=ft.Text("Resultado")),
                ft.DataColumn(label=ft.Text("Criado em")),
                ft.DataColumn(label=ft.Text("Ação")),
            ],
            rows=rows,
            heading_row_height=40,
            data_row_min_height=40,
            column_spacing=10,
        )

        self.controls = [
            ft.Container(
                content=table,
                expand=True,
                bgcolor=ft.Colors.WHITE,
                padding=10,
                border_radius=10,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            )
        ]
