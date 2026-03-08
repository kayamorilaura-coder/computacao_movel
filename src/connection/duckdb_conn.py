import duckdb

class DatabaseCalculator():
    def init(self):
        self.connection()
    
    def connection():
        conn = duckdb.connect("historico.parquet")
        conn.execute("""CREATE TABLE IF NOT EXISTS history ( 
                    id BIGINT PRIMARY KEY, 
                    expression TEXT NOT NULL,
                    result TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );""")
        conn.close()

    def apagar_um_inserir(self):
        pass

    def total_registro(self):
        self.connection()
        quantidade = conn.execute("""
                                    SELECT COUNT(*) AS total
FROM read_parquet('caminho/do/historico.parquet')
                                """)

        

    def inserir(self):
        pass
