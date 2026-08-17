"""Módulo de Gestão de Pessoas e Colaboradores - GW Factory."""

from typing import Dict, List


class Pessoa:
    """Representa a estrutura de dados e perfil de um colaborador."""

    def __init__(
        self,
        nome: str,
        cargo: str,
        email: str,
        telefone: str,
        data_admissao: str,
        projeto: str,
        senha: str,
    ):
        self.nome: str = nome
        self.cargo: str = cargo
        self.email: str = email
        self.telefone: str = telefone
        self.data_admissao: str = data_admissao
        self.projeto: str = projeto
        self.senha: str = senha

    def exibir_dados(self) -> str:
        """Retorna uma string formatada ocultando a senha real."""
        senha_oculta = (
            "*" * len(self.senha) if self.senha else "Não cadastrada."
        )
        return (
            f"Nome: {self.nome} | Cargo: {self.cargo} | E-mail: {self.email} | "
            f"Telefone: {self.telefone} | Data Admissão: {self.data_admissao} | "
            f"Projeto: {self.projeto} | Senha: {senha_oculta}"
        )

    def para_dicionario(self) -> Dict[str, str]:
        """Converte a instância do objeto para dicionário Python."""
        return {
            "nome": self.nome,
            "cargo": self.cargo,
            "email": self.email,
            "telefone": self.telefone,
            "data_admissao": self.data_admissao,
            "projeto": self.projeto,
            "senha": self.senha,
        }


class GerenciadorPessoas:
    """Gerencia as operações de cadastro e busca de colaboradores na memória."""

    def __init__(self):
        self.pessoas: List[Pessoa] = []

    # 1. CRIAR
    def adicionar(self, pessoa: Pessoa) -> None:
        """Adiciona um novo colaborador à lista."""
        self.pessoas.append(pessoa)

    # 2. LER / LISTAR
    def listar_todas(self) -> None:
        """Exibe no terminal todas as pessoas cadastradas."""
        if not self.pessoas:
            print("Nenhuma Pessoa Cadastrada")
            return

        print("\n-- LISTA COMPLETA DE PESSOAS --")
        for pessoa in self.pessoas:
            print(pessoa.exibir_dados())

    def listar_todas_como_dicionario(self) -> List[Dict[str, str]]:
        """Retorna a lista de pessoas em formato de dicionário para integração Web."""
        return [p.para_dicionario() for p in self.pessoas]

    def cadastrar_interativo(self) -> None:
        """Realiza o cadastro interativo via terminal."""
        print("\n --- NOVO CADASTRO DE PESSOA ---\n")
        nome = input("Digite o nome completo: ").strip()
        cargo = input("Digite o cargo: ").strip()
        email = input("Digite o e-mail: ").strip()
        telefone = input("Digite o telefone: ").strip()
        data_admissao = input("Digite a data de admissão: ").strip()
        projeto = input("Digite o nome do projeto: ").strip()
        senha = input("Digite uma senha: ").strip()

        nova_pessoa = Pessoa(
            nome, cargo, email, telefone, data_admissao, projeto, senha
        )
        self.adicionar(nova_pessoa)
        print(f"Pessoa '{nome}' adicionada com sucesso!")

    # 3. BUSCAR
    def buscar_nome(self, termo: str) -> List[Pessoa]:
        """Busca colaboradores contendo o termo informado no nome."""
        termo_lower = termo.lower().strip()
        return [p for p in self.pessoas if termo_lower in p.nome.lower()]

    # 4. FILTRAR
    def filtrar_por_projeto(self, nome_projeto: str) -> List[Pessoa]:
        """Filtra colaboradores por projeto (suporta múltiplos projetos)."""
        proj_lower = nome_projeto.lower().strip()
        return [p for p in self.pessoas if proj_lower in p.projeto.lower()]

    # 5. REMOVER
    def remover_por_email(self, email: str) -> bool:
        """Remove um colaborador a partir do e-mail cadastrado."""
        email_lower = email.lower().strip()
        for pessoa in self.pessoas:
            if pessoa.email.lower() == email_lower:
                self.pessoas.remove(pessoa)
                print(f"Pessoa com e-mail '{email}' removida com sucesso!")
                return True
        print(f"Nenhuma pessoa encontrada com o e-mail '{email}'.")
        return False