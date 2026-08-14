import sqlite3
import os


class DatabaseManager:
    def __init__(self, db_name="chamados_factory.db"):
        # Garante que o banco seja salvo na raiz do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, db_name)
        self.criar_tabelas()

    def conectar(self):
        return sqlite3.connect(self.db_path)

    def criar_tabelas(self):
        """Cria a tabela de chamados caso ela ainda não exista."""
        query = """
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitante TEXT,
            projeto TEXT,
            categoria TEXT,
            subcategoria TEXT,
            patrimonio TEXT,
            andar_sala TEXT,
            ip TEXT,
            resumo TEXT,
            descricao TEXT,
            impacto TEXT,
            data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def salvar_chamado(self, dados_chamado: dict):
        """Salva um novo chamado no banco de dados."""
        query = """
        INSERT INTO chamados (
            solicitante, projeto, categoria, subcategoria, 
            patrimonio, andar_sala, ip, resumo, descricao, impacto
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            dados_chamado.get("solicitante", ""),
            dados_chamado.get("projeto", ""),
            dados_chamado.get("categoria", ""),
            dados_chamado.get("subcategoria", ""),
            dados_chamado.get("patrimonio", ""),
            dados_chamado.get("andar_sala", ""),
            dados_chamado.get("ip", ""),
            dados_chamado.get("resumo", ""),
            dados_chamado.get("descricao", ""),
            dados_chamado.get("impacto", "")
        )

        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            return cursor.lastrowid  # Retorna o ID gerado (Ex: Chamado #12)

    def listar_chamados(self):
        """Busca todos os chamados para mostrar na tela depois."""
        query = "SELECT * FROM chamados ORDER BY data_abertura DESC"
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            # Pega os nomes das colunas para montar um dicionário
            colunas = [descricao[0] for descricao in cursor.description]
            linhas = cursor.fetchall()

            # Transforma a resposta do banco em uma lista de dicionários fáceis de ler
            return [dict(zip(colunas, linha)) for linha in linhas]