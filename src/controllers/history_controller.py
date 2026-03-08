from connection.duckdb_conn import DatabaseCalculator

# Vai em self tudo que pertence ao objeto e que pode ser 
# reutilizado por mais do que um metódo
class HistoryController:
    def init(self):
        self.db_connection =  DatabaseCalculator()
        
    def save(self, resultado, result):
        limite = self.db_connection.total_registro()
        if limite >= 10:
            self.db_connection.apagar_um_inserir()
        else:
            self.db_connection.inserir()

