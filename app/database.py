import sqlite3


class DatabaseManager:

    def __init__(self, db_name="chamados_factory.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        """Abre a conexão com o arquivo do banco SQLite."""
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Cria as tabelas necessárias no banco de dados caso não existam."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Tabela de Chamados
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chamados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    protocolo TEXT,
                    solicitante TEXT,
                    projeto TEXT,
                    categoria TEXT,
                    subcategoria TEXT,
                    resumo TEXT,
                    patrimonio TEXT,
                    andar_sala TEXT,
                    ip TEXT,
                    descricao TEXT,
                    impacto TEXT,
                    prazo_sla TEXT,
                    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 🟢 2. NOVA TABELA: Pessoas / Colaboradores Persistentes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pessoas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cargo TEXT,
                    email TEXT UNIQUE NOT NULL,
                    telefone TEXT,
                    data_admissao TEXT,
                    projeto TEXT,
                    senha TEXT NOT NULL
                )
            """)
            conn.commit()

        # Insere os dados de teste iniciais apenas se a tabela estiver vazia
        self._inserir_pessoas_iniciais()

    def _inserir_pessoas_iniciais(self):
        """Cadastra os usuários padrão caso o banco esteja novo."""
        if len(self.listar_pessoas()) == 0:
            p1 = {
                "nome": "Charles Ferreira de Moura",
                "cargo": "Dev Junior",
                "email": "charles@empresa.com",
                "telefone": "61 9999-9999",
                "data_admissao": "01/08/2024",
                "projeto": "MCTI, COPASA",
                "senha": "123",
            }
            p2 = {
                "nome": "Ana Carolina",
                "cargo": "Analista de Dados",
                "email": "ana@colaboradores.empresa.com",
                "telefone": "61 9991-1234",
                "data_admissao": "01/01/2026",
                "projeto": "MEC",
                "senha": "123",
            }
            self.salvar_pessoa(p1)
            self.salvar_pessoa(p2)

    # ==========================================================================
    # 👤 MÉTODOS DE PESSOAS (PERSISTÊNCIA)
    # ==========================================================================
    def salvar_pessoa(self, pessoa_dict):
        """Insere um novo colaborador no banco SQLite."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO pessoas (nome, cargo, email, telefone, data_admissao, projeto, senha)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    pessoa_dict["nome"],
                    pessoa_dict["cargo"],
                    pessoa_dict["email"],
                    pessoa_dict["telefone"],
                    pessoa_dict["data_admissao"],
                    pessoa_dict["projeto"],
                    pessoa_dict["senha"],
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def listar_pessoas(self):
        """Retorna todas as pessoas cadastradas no banco como uma lista de dicionários."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pessoas ORDER BY nome ASC")
            linhas = cursor.fetchall()
            return [dict(linha) for linha in linhas]

    def buscar_pessoa_por_login(self, email, senha):
        """Valida e-mail e senha no banco de dados para realizar o login."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM pessoas WHERE LOWER(email) = LOWER(?) AND senha = ?",
                (email.strip(), senha),
            )
            linha = cursor.fetchone()
            return dict(linha) if linha else None

    # ==========================================================================
    # 🎫 MÉTODOS DE CHAMADOS
    # ==========================================================================
    def salvar_chamado(self, chamado):
        """Insere um novo chamado no banco de dados."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chamados (protocolo, solicitante, projeto, categoria, subcategoria, resumo, patrimonio, andar_sala, ip, descricao, impacto, prazo_sla)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    chamado.get("protocolo"),
                    chamado.get("solicitante"),
                    chamado.get("projeto"),
                    chamado.get("categoria"),
                    chamado.get("subcategoria"),
                    chamado.get("resumo"),
                    chamado.get("patrimonio"),
                    chamado.get("andar_sala"),
                    chamado.get("ip"),
                    chamado.get("descricao"),
                    chamado.get("impacto"),
                    chamado.get("prazo_sla"),
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def obter_proximo_id(self):
        """Retorna o próximo ID incremental para gerar o protocolo amigável."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT seq FROM sqlite_sequence WHERE name='chamados'"
            )
            linha = cursor.fetchone()
            return (linha[0] + 1) if linha else 1

    def listar_chamados(self):
        """Retorna a lista completa de chamados em ordem do mais recente para o mais antigo."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chamados ORDER BY id DESC")
            linhas = cursor.fetchall()
            return [dict(linha) for linha in linhas]