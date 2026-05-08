import duckdb
import flet as ft
from datetime import datetime
import os

PARQUET_FILE = "historico.parquet"


class DatabaseCalculator:
    def __init__(self):
        self._init_storage()

    def _init_storage(self):
        # Garante que o ficheiro parquet existe com o schema certo
        conn = duckdb.connect()
        conn.execute("""
            CREATE TABLE history (
                id BIGINT,
                expression TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        if os.path.exists(PARQUET_FILE):
            # Se já existir, anexar os dados atuais
            conn.execute(f"""
                INSERT INTO history
                SELECT * FROM read_parquet('{PARQUET_FILE}');
            """)
        # Escreve ou sobreescreve o parquet com o schema correto
        conn.execute(f"""
            COPY history TO '{PARQUET_FILE}' (FORMAT 'parquet');
        """)
        conn.close()

    def connection(self):
        # Conexão em memória, lendo o parquet
        conn = duckdb.connect()
        conn.execute(f"""
            CREATE TABLE history AS
            SELECT * FROM read_parquet('{PARQUET_FILE}');
        """)
        return conn

    def total_registro(self) -> int:
        conn = self.connection()
        total = conn.execute("SELECT COUNT(*) FROM history;").fetchone()[0]
        conn.close()
        return total

    def inserir(self, expression: str, result: str):
        # Insere uma nova linha gerando id e timestamp
        conn = self.connection()
        next_id = conn.execute("SELECT COALESCE(MAX(id) + 1, 1) FROM history;").fetchone()[0]
        created_at = datetime.now()

        conn.execute(
            "INSERT INTO history (id, expression, result, created_at) VALUES (?, ?, ?, ?);",
            (next_id, expression, result, created_at),
        )

        # Regrava o parquet com os novos dados
        conn.execute(f"COPY history TO '{PARQUET_FILE}' (FORMAT 'parquet');")
        conn.close()

    def apagar_um_inserir(self, expression: str, result: str):
        # Exemplo: apaga o registo mais antigo e insere um novo
        conn = self.connection()
        oldest = conn.execute(
            "SELECT id FROM history ORDER BY created_at ASC LIMIT 1;"
        ).fetchone()
        if oldest:
            conn.execute("DELETE FROM history WHERE id = ?;", (oldest[0],))
        # Depois insere o novo
        next_id = conn.execute("SELECT COALESCE(MAX(id) + 1, 1) FROM history;").fetchone()[0]
        created_at = datetime.now()
        conn.execute(
            "INSERT INTO history (id, expression, result, created_at) VALUES (?, ?, ?, ?);",
            (next_id, expression, result, created_at),
        )
        conn.execute(f"COPY history TO '{PARQUET_FILE}' (FORMAT 'parquet');")
        conn.close()

    def listar_historico(self):
        conn = self.connection()
        rows = conn.execute(
            "SELECT id, expression, result, created_at FROM history ORDER BY created_at DESC;"
        ).fetchall()
        conn.close()
        return rows
    
    def deletar_por_id(self, id_: int):
        conn = self.connection()
        conn.execute("DELETE FROM history WHERE id = ?;", (id_,))
        conn.execute(f"COPY history TO '{PARQUET_FILE}' (FORMAT 'parquet');")
        conn.close()
    
    def sync_to_client(self):
        if not self.page:
            return
        
        try:
            rows = self.listar_historico()  # Pega dados do Parquet
            history = [{"id": r[0], "expression": r[1], "result": r[2], "created_at": str(r[3])} for r in rows]
            
            # Salva no Client Storage como JSON
            self.page.client_storage.set("calc_history", json.dumps(history))
            print("Sincronizado DuckDB → Client Storage")
        except Exception as e:
            print(f"Erro sync: {e}")


 



def main(page: ft.Page):
    page.title = "Historico DuckDB + Parquet"
    db = DatabaseCalculator()

    expression_field = ft.TextField(label="Expressão", width=300)
    result_field = ft.TextField(label="Resultado", width=300)
    total_text = ft.Text(f"Total de registos: {db.total_registro()}")

    def atualizar_total():
        total_text.value = f"Total de registos: {db.total_registro()}"
        page.update()

    def on_inserir_click(e):
        if expression_field.value and result_field.value:
            db.inserir(expression_field.value, result_field.value)
            expression_field.value = ""
            result_field.value = ""
            atualizar_total()

    def on_apagar_um_inserir(e):
        if expression_field.value and result_field.value:
            db.apagar_um_inserir(expression_field.value, result_field.value)
            expression_field.value = ""
            result_field.value = ""
            atualizar_total()

    btn_inserir = ft.ElevatedButton("Inserir", on_click=on_inserir_click)
    btn_apagar_inserir = ft.ElevatedButton("Apagar um e inserir", on_click=on_apagar_um_inserir)

    page.add(
        ft.Column(
            controls=[
                expression_field,
                result_field,
                ft.Row([btn_inserir, btn_apagar_inserir]),
                total_text,
            ]
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
