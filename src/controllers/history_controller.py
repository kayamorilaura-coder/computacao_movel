from connection.duckdb_conn import DatabaseCalculator
from connection.client_storage import ClientStorageCalculator

class HistoryController:
    def __init__(self):
        self.db_connection = DatabaseCalculator()
        #self.cs_connection = ClientStorageCalculator()  # Precisa page!

    def save(self, expression: str, result: str):
        try:
            limite = self.db_connection.total_registro()
        except Exception:
            print("Cliente Storage")
            #limite = self.cs_connection.total_registro()
        
        if limite >= 10:
            self.db_connection.apagar_um_inserir(expression, result)
            #self.cs_connection.apagar_um_inserir(expression, result)  # Sync CS
        else:
            self.db_connection.inserir(expression, result)
            #self.cs_connection.inserir(expression, result)  # Sync CS

    def list(self):
        try:
            return self.db_connection.listar_historico()
        except Exception:
            #return self.cs_connection.listar_historico()  # Fallback CS
            print("Cliente Storage")

    def delete(self, id_: int):
        try:
            self.db_connection.deletar_por_id(id_)
            #self.cs_connection.deletar_por_id(id_)  # Sync CS
        except Exception:
            print("Cliente Storage")

    def copy_row(self, row):
        # row é tuple do DB ou dict do CS → adapta
        if isinstance(row, tuple):
            texto = f"ID: {row[0]} | Expressão: {row[1]} | Resultado: {row[2]} | Data: {row[3]}"
        else:  # dict do CS
            texto = f"ID: {row['id']} | Expressão: {row['expression']} | Resultado: {row['result']} | Data: {row['created_at']}"
        return texto
