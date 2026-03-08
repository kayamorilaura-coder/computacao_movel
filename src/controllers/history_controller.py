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
        

    def delete():
        pass

    def update():
        pass