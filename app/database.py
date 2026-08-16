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

    # ==========================================================================
    # ✏️ ATUALIZAÇÃO DE CADASTRO DE PESSOA (SQLITE)
    # ==========================================================================
    def atualizar_pessoa(self, id_pessoa, pessoa_dict):
        """Atualiza os dados de um colaborador existente pelo ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE pessoas 
                SET nome = ?, cargo = ?, email = ?, telefone = ?, data_admissao = ?, projeto = ?
                WHERE id = ?
            """,
                (
                    pessoa_dict["nome"],
                    pessoa_dict["cargo"],
                    pessoa_dict["email"],
                    pessoa_dict["telefone"],
                    pessoa_dict["data_admissao"],
                    pessoa_dict["projeto"],
                    id_pessoa,
                ),
            )
            conn.commit()
            return cursor.rowcount

        # ==========================================================================
        # 🔑 ALTERAÇÃO DE SENHA (SQLITE)
        # ==========================================================================

    def alterar_senha_pessoa(self, id_pessoa, nova_senha):
        """Atualiza a senha de um colaborador pelo ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE pessoas 
                SET senha = ?
                WHERE id = ?
            """,
                (nova_senha, id_pessoa),
            )
            conn.commit()
            return cursor.rowcount

        # ==========================================================================
        # 🎫 FINALIZAÇÃO E ATUALIZAÇÃO DE CHAMADO (SQLITE)
        # ==========================================================================

    def finalizar_chamado(
            self,
            id_chamado,
            status,
            motivo_finalizacao,
            parecer_operador,
            parecer_torre,
    ):
        """Grava a resolução do chamado com os pareceres do operador e da torre externa."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Garante que as colunas existam ou atualiza os dados
            cursor.execute(
                """
                UPDATE chamados 
                SET status = ?, 
                    motivo_finalizacao = ?, 
                    solucao_operador = ?, 
                    solucao_torre = ?
                WHERE id = ?
            """,
                (
                    status,
                    motivo_finalizacao,
                    parecer_operador,
                    parecer_torre,
                    id_chamado,
                ),
            )
            conn.commit()
            return cursor.rowcount

        # ==========================================================================
        # 👥 GERADOR DE SERVIDORES / CLIENTES AUTOMÁTICOS POR PROJETO
        # ==========================================================================

    def popular_clientes_automaticos(self):
        """Popula o banco com cerca de 20 servidores/clientes caso a base esteja vazia."""
        pessoas_existentes = self.listar_pessoas()
        if len(pessoas_existentes) > 2:
            return  # Já possui cadastros suficientes

        clientes_iniciais = [
            # MCTI - Ministério da Ciência, Tecnologia e Inovações
            {"nome": "Dra. Maria Helena Souza", "cargo": "Coordenadora de Pesquisa",
             "email": "maria.souza@mcti.gov.br", "telefone": "(61) 98111-2001", "data_admissao": "10/01/2019",
             "projeto": "MCTI"},
            {"nome": "Roberto Carlos Andrade", "cargo": "Analista em C&T", "email": "roberto.andrade@mcti.gov.br",
             "telefone": "(61) 98111-2002", "data_admissao": "15/03/2020", "projeto": "MCTI"},
            {"nome": "Patricia Lima e Silva", "cargo": "Chefe de Gabinete", "email": "patricia.silva@mcti.gov.br",
             "telefone": "(61) 98111-2003", "data_admissao": "01/02/2018", "projeto": "MCTI"},
            {"nome": "Fernando Dias Santos", "cargo": "Técnico Administrativo",
             "email": "fernando.santos@mcti.gov.br", "telefone": "(61) 98111-2004", "data_admissao": "20/06/2021",
             "projeto": "MCTI"},

            # COPASA - Companhia de Saneamento de MG
            {"nome": "Eng. Gustavo Barbosa", "cargo": "Engenheiro Operacional",
             "email": "gustavo.barbosa@copasa.com.br", "telefone": "(31) 99222-3001", "data_admissao": "12/04/2017",
             "projeto": "COPASA"},
            {"nome": "Juliana Martins Costa", "cargo": "Supervisora de Estação",
             "email": "juliana.costa@copasa.com.br", "telefone": "(31) 99222-3002", "data_admissao": "05/08/2020",
             "projeto": "COPASA"},
            {"nome": "Marcelo Resende Viana", "cargo": "Técnico de Saneamento",
             "email": "marcelo.viana@copasa.com.br", "telefone": "(31) 99222-3003", "data_admissao": "11/11/2022",
             "projeto": "COPASA"},
            {"nome": "Luciana Ribeiro Neves", "cargo": "Analista Financeira",
             "email": "luciana.neves@copasa.com.br", "telefone": "(31) 99222-3004", "data_admissao": "03/01/2021",
             "projeto": "COPASA"},

            # MEC - Ministério da Educação
            {"nome": "Prof. Eduardo Oliveira", "cargo": "Diretor de Programas",
             "email": "eduardo.oliveira@mec.gov.br", "telefone": "(61) 98333-4001", "data_admissao": "02/05/2016",
             "projeto": "MEC"},
            {"nome": "Camila Guimarães Rocha", "cargo": "Coordenadora Pedagógica",
             "email": "camila.rocha@mec.gov.br", "telefone": "(61) 98333-4002", "data_admissao": "14/09/2019",
             "projeto": "MEC"},
            {"nome": "Rodrigo Mendes Faria", "cargo": "Analista de Políticas Públicas",
             "email": "rodrigo.faria@mec.gov.br", "telefone": "(61) 98333-4003", "data_admissao": "08/07/2021",
             "projeto": "MEC"},
            {"nome": "Aline Castro Vasconcelos", "cargo": "Secretária Executiva",
             "email": "aline.castro@mec.gov.br", "telefone": "(61) 98333-4004", "data_admissao": "19/10/2020",
             "projeto": "MEC"},

            # START CAOA
            {"nome": "Thiago Alcantara Monteiro", "cargo": "Gerente de Vendas",
             "email": "thiago.monteiro@startcaoa.com.br", "telefone": "(11) 97444-5001",
             "data_admissao": "01/03/2022", "projeto": "START CAOA"},
            {"nome": "Vanessa Teixeira Prado", "cargo": "Consultora de Pós-Venda",
             "email": "vanessa.prado@startcaoa.com.br", "telefone": "(11) 97444-5002",
             "data_admissao": "15/01/2023", "projeto": "START CAOA"},
            {"nome": "Bruno Henrique Xavier", "cargo": "Supervisor de Peças",
             "email": "bruno.xavier@startcaoa.com.br", "telefone": "(11) 97444-5003", "data_admissao": "10/08/2021",
             "projeto": "START CAOA"},
            {"nome": "Beatriz Nogueira Ramos", "cargo": "Analista de Garantia",
             "email": "beatriz.ramos@startcaoa.com.br", "telefone": "(11) 97444-5004",
             "data_admissao": "04/04/2022", "projeto": "START CAOA"},

            # GLOBALWEB (Interno / Matriz)
            {"nome": "Alexandre Pires Toledo", "cargo": "Gerente de Contratos",
             "email": "alexandre.toledo@globalweb.com.br", "telefone": "(61) 99555-6001",
             "data_admissao": "01/01/2018", "projeto": "Globalweb"},
            {"nome": "Daniela Freitas Borges", "cargo": "Coordenadora de Service Desk",
             "email": "daniela.borges@globalweb.com.br", "telefone": "(61) 99555-6002",
             "data_admissao": "12/06/2020", "projeto": "Globalweb"},
            {"nome": "Gabriel Junqueira Paiva", "cargo": "Especialista de Infraestrutura",
             "email": "gabriel.paiva@globalweb.com.br", "telefone": "(61) 99555-6003",
             "data_admissao": "03/09/2021", "projeto": "Globalweb"},
            {"nome": "Fernanda Esteves Garcia", "cargo": "Analista de Qualidade",
             "email": "fernanda.garcia@globalweb.com.br", "telefone": "(61) 99555-6004",
             "data_admissao": "18/02/2023", "projeto": "Globalweb"}
        ]

        for c in clientes_iniciais:
            c["senha"] = "123456"
            self.salvar_pessoa(c)
