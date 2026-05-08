import json
import flet as ft
from datetime import datetime

class ClientStorageCalculator:
    def __init__(self, page):
        self.page = page
        self.history = []
        self.load_history()

    def load_history(self):
        """Carrega histórico do Client Storage"""
        try:
            hist_json = self.page.client_storage.get("calc_history")
            if hist_json:
                self.history = json.loads(hist_json)
        except:
            self.history = []

    def total_registro(self) -> int:
        """Conta total de registos (igual ao DuckDB)"""
        return len(self.history)

    def inserir(self, expression: str, result: str):
        """Insere novo registo (igual ao DuckDB)"""
        # Gera ID sequencial como no DuckDB
        next_id = len(self.history) + 1
        created_at = datetime.now().isoformat()
        
        new_entry = {
            "id": next_id,
            "expression": expression,
            "result": result,
            "created_at": created_at
        }
        
        self.history.insert(0, new_entry)  # Mais recente primeiro
        self._save()  # Salva no Client Storage

    def apagar_um_inserir(self, expression: str, result: str):
        """Apaga mais antigo e insere novo (igual ao DuckDB)"""
        # Apaga mais antigo (último da lista)
        if self.history:
            self.history.pop()  # Remove último
        
        # Insere novo
        self.inserir(expression, result)

    def listar_historico(self):
        """Lista histórico ordenado por data DESC (igual ao DuckDB)"""
        # Já está ordenado (mais recente primeiro)
        return self.history

    def deletar_por_id(self, id_: int):
        """Deleta por ID (igual ao DuckDB)"""
        self.history = [h for h in self.history if h["id"] != id_]
        self._save()

    def _save(self):
        """Salva no Client Storage (interno)"""
        self.page.client_storage.set("calc_history", json.dumps(self.history))
