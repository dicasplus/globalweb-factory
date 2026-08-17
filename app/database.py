"""Módulo de Gerenciamento do Banco de Dados SQLite do GlobalWeb Factory.

Gerencia persistência de chamados, pessoas/colaboradores e migrações de colunas.
"""

from datetime import datetime
import sqlite3
from typing import Any, Dict, List, Optional


class DatabaseManager:
    """Gerenciador de banco de dados SQLite para o sistema GlobalWeb Factory."""

    def __init__(self, db_name: str = "chamados_factory.db"):
        self.db_name: str = db_name
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Abre e retorna a conexão com o banco SQLite."""
        return sqlite3.connect(self.db_name)

    def init_db(self) -> None:
        """Cria as tabelas necessárias e executa migrações automáticas de colunas."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Tabela de Chamados com suporte a todas as colunas
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chamados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    protocolo TEXT,
                    solicitante TEXT,
                    email TEXT,
                    projeto TEXT,
                    categoria TEXT,
                    subcategoria TEXT,
                    resumo TEXT,
                    patrimonio TEXT,
                    andar_sala TEXT,
                    ip TEXT,
                    descricao TEXT,
                    impacto TEXT,
                    operador TEXT,
                    status TEXT DEFAULT 'Aberto',
                    prazo_sla TEXT,
                    data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # Migrações automáticas de colunas para bancos SQLite legados
            cursor.execute("PRAGMA table_info(chamados)")
            colunas_existentes = [col[1] for col in cursor.fetchall()]

            migracao_colunas = {
                "status": "ALTER TABLE chamados ADD COLUMN status TEXT DEFAULT 'Aberto'",
                "operador": "ALTER TABLE chamados ADD COLUMN operador TEXT",
                "email": "ALTER TABLE chamados ADD COLUMN email TEXT",
            }

            for col_nome, sql_alter in migracao_colunas.items():
                if col_nome not in colunas_existentes:
                    cursor.execute(sql_alter)

            # 2. Tabela de Pessoas / Colaboradores Persistentes
            cursor.execute(
                """
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
                """
            )
            conn.commit()

        # Insere usuários padrão apenas se a base estiver vazia
        self._inserir_pessoas_iniciais()

    def _inserir_pessoas_iniciais(self) -> None:
        """Cadastra colaboradores padrão caso o banco esteja novo."""
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
    def salvar_pessoa(self, pessoa_dict: Dict[str, Any]) -> Optional[int]:
        """Insere um novo colaborador no banco SQLite."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO pessoas (nome, cargo, email, telefone, data_admissao, projeto, senha)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    pessoa_dict.get("nome"),
                    pessoa_dict.get("cargo"),
                    pessoa_dict.get("email"),
                    pessoa_dict.get("telefone"),
                    pessoa_dict.get("data_admissao"),
                    pessoa_dict.get("projeto"),
                    pessoa_dict.get("senha"),
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def listar_pessoas(self) -> List[Dict[str, Any]]:
        """Retorna todas as pessoas cadastradas como lista de dicionários."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pessoas ORDER BY nome ASC")
            linhas = cursor.fetchall()
            return [{str(k): row[k] for k in row.keys()} for row in linhas]

    def buscar_pessoa_por_login(
        self, email: str, senha: str
    ) -> Optional[Dict[str, Any]]:
        """Valida e-mail e senha para realizar login."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM pessoas WHERE LOWER(email) = LOWER(?) AND senha = ?",
                (email.strip(), senha),
            )
            linha = cursor.fetchone()
            if linha:
                return {str(k): linha[k] for k in linha.keys()}
            return None

    def atualizar_pessoa(
        self, id_pessoa: int, pessoa_dict: Dict[str, Any]
    ) -> int:
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
                    pessoa_dict.get("nome"),
                    pessoa_dict.get("cargo"),
                    pessoa_dict.get("email"),
                    pessoa_dict.get("telefone"),
                    pessoa_dict.get("data_admissao"),
                    pessoa_dict.get("projeto"),
                    id_pessoa,
                ),
            )
            conn.commit()
            return cursor.rowcount

    def alterar_senha_pessoa(self, id_pessoa: int, nova_senha: str) -> int:
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
    # 🎫 MÉTODOS DE CHAMADOS
    # ==========================================================================
    def salvar_chamado(self, chamado: Dict[str, Any]) -> Optional[int]:
        """Insere um novo chamado no banco de dados incluindo operador e e-mail."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chamados (
                    protocolo, solicitante, email, projeto, categoria, subcategoria, 
                    resumo, patrimonio, andar_sala, ip, descricao, impacto, 
                    operador, status, prazo_sla
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    chamado.get("protocolo"),
                    chamado.get("solicitante"),
                    chamado.get("email"),
                    chamado.get("projeto"),
                    chamado.get("categoria"),
                    chamado.get("subcategoria"),
                    chamado.get("resumo"),
                    chamado.get("patrimonio"),
                    chamado.get("andar_sala"),
                    chamado.get("ip"),
                    chamado.get("descricao"),
                    chamado.get("impacto"),
                    chamado.get("operador"),
                    chamado.get("status", "Aberto"),
                    chamado.get("prazo_sla"),
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def obter_proximo_id(self) -> int:
        """Retorna o próximo ID incremental para gerar o protocolo."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT seq FROM sqlite_sequence WHERE name='chamados'"
            )
            linha = cursor.fetchone()
            return (linha[0] + 1) if linha else 1

    def listar_chamados(self) -> List[Dict[str, Any]]:
        """Retorna todos os chamados em ordem do mais recente para o mais antigo."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chamados ORDER BY id DESC")
            linhas = cursor.fetchall()
            return [{str(k): row[k] for k in row.keys()} for row in linhas]

    def atualizar_status_chamado(
        self, chamado_id: int, novo_status: str, solucao: str = ""
    ) -> bool:
        """Atualiza o status do chamado e anexa o parecer técnico se houver."""
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

        texto_adicional = ""
        if solucao and solucao.strip():
            texto_adicional = (
                f"\n\n--- 🏁 PARECER DE FECHAMENTO ({data_hora}) ---\n"
                f"{solucao.strip()}"
            )

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE chamados
                SET status = ?,
                    descricao = descricao || ?
                WHERE id = ?
                """,
                (novo_status, texto_adicional, chamado_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def adicionar_comentario_chamado(
        self, chamado_id: int, autor: str, comentario: str
    ) -> bool:
        """Registra novo comentário formatado na linha do tempo do chamado."""
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

        texto_comentario = (
            f"\n\n--- 💬 COMENTÁRIO [{data_hora}] ({autor}) ---\n"
            f"{comentario.strip()}"
        )

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE chamados
                SET descricao = descricao || ?
                WHERE id = ?
                """,
                (texto_comentario, chamado_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def finalizar_chamado(
        self,
        id_chamado: int,
        status: str,
        motivo_finalizacao: str,
        parecer_operador: str,
        parecer_torre: str,
    ) -> int:
        """Grava a resolução legada do chamado."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
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
    # 👥 GERADOR DE CLIENTES/SERVIDORES AUTOMÁTICOS
    # ==========================================================================
    def popular_clientes_automaticos(self) -> None:
        """Popula o banco com servidores/clientes caso a base esteja nova."""
        pessoas_existentes = self.listar_pessoas()
        if len(pessoas_existentes) > 2:
            return

        clientes_iniciais = [
            {
                "nome": "Dra. Maria Helena Souza",
                "cargo": "Coordenadora de Pesquisa",
                "email": "maria.souza@mcti.gov.br",
                "telefone": "(61) 98111-2001",
                "data_admissao": "10/01/2019",
                "projeto": "MCTI",
            },
            {
                "nome": "Roberto Carlos Andrade",
                "cargo": "Analista em C&T",
                "email": "roberto.andrade@mcti.gov.br",
                "telefone": "(61) 98111-2002",
                "data_admissao": "15/03/2020",
                "projeto": "MCTI",
            },
            {
                "nome": "Eng. Gustavo Barbosa",
                "cargo": "Engenheiro Operacional",
                "email": "gustavo.barbosa@copasa.com.br",
                "telefone": "(31) 99222-3001",
                "data_admissao": "12/04/2017",
                "projeto": "COPASA",
            },
            {
                "nome": "Prof. Eduardo Oliveira",
                "cargo": "Diretor de Programas",
                "email": "eduardo.oliveira@mec.gov.br",
                "telefone": "(61) 98333-4001",
                "data_admissao": "02/05/2016",
                "projeto": "MEC",
            },
        ]

        for c in clientes_iniciais:
            c["senha"] = "123456"
            self.salvar_pessoa(c)