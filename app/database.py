import os
import sqlite3


class DatabaseManager:

    def __init__(self, db_name="chamados_factory.db"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, db_name)
        self.criar_tabelas()

    def conectar(self):
        return sqlite3.connect(self.db_path)

    def criar_tabelas(self):
        """Cria e atualiza as tabelas do banco de dados."""
        query = """
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            protocolo TEXT,
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
            prazo_sla TEXT,
            data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query)

            # garante que colunas novas existam em bancos antigos
            cursor.execute("PRAGMA table_info(chamados)")
            colunas = [col[1] for col in cursor.fetchall()]

            if "protocolo" not in colunas:
                cursor.execute("ALTER TABLE chamados ADD COLUMN protocolo TEXT")
            if "prazo_sla" not in colunas:
                cursor.execute("ALTER TABLE chamados ADD COLUMN prazo_sla TEXT")

            conn.commit()

    def obter_proximo_id(self):
        """Retorna o próximo ID incremental para montar o número do protocolo."""
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id) FROM chamados")
            ultimo_id = cursor.fetchone()[0]
            return (ultimo_id or 0) + 1

    def salvar_chamado(self, dados_chamado: dict):
        """Salva um novo chamado no banco de dados."""
        query = """
        INSERT INTO chamados (
            protocolo, solicitante, projeto, categoria, subcategoria, 
            patrimonio, andar_sala, ip, resumo, descricao, impacto, prazo_sla
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            dados_chamado.get("protocolo", ""),
            dados_chamado.get("solicitante", ""),
            dados_chamado.get("projeto", ""),
            dados_chamado.get("categoria", ""),
            dados_chamado.get("subcategoria", ""),
            dados_chamado.get("patrimonio", ""),
            dados_chamado.get("andar_sala", ""),
            dados_chamado.get("ip", ""),
            dados_chamado.get("resumo", ""),
            dados_chamado.get("descricao", ""),
            dados_chamado.get("impacto", "Baixo"),
            dados_chamado.get("prazo_sla", "24 horas"),
        )

        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            return cursor.lastrowid

    def listar_chamados(self):
        """Busca todos os chamados salvos."""
        query = "SELECT * FROM chamados ORDER BY id DESC"
        with self.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            colunas = [descricao[0] for descricao in cursor.description]
            linhas = cursor.fetchall()
            return [dict(zip(colunas, linha)) for linha in linhas]