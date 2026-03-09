from connection.duckdb_conn import DatabaseCalculator

class HistoryController:
    def __init__(self):
        self.db_connection = DatabaseCalculator()

    def save(self, expression: str, result: str):
        limite = self.db_connection.total_registro()
        if limite >= 10:
            self.db_connection.apagar_um_inserir(expression, result)
        else:
            self.db_connection.inserir(expression, result)

    def list(self):
        return self.db_connection.listar_historico()
        

    def delete(self, id_:int):
        self.db_connection.deletar_por_id(id_)

    def copy_row(self, row):
        texto = row #f"ID: {row[0]} | Expressão: {row[1]} | Resultado: {row[2]} | Data: {row[3]}"
        return texto