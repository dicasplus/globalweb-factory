class Pessoa:
    def __init__(self, nome, cargo, email, telefone, data_admissao, projeto, senha):
        self.nome = nome
        self.cargo = cargo
        self.email = email
        self.telefone = telefone
        self.data_admissao = data_admissao
        self.projeto = projeto
        self.senha = senha

    def exibir_dados(self):
        #mascarar senha com astericos para nao expor a senha em prints aleatorios
        senha_oculta = "*" * len(self.senha) if self.senha else "Não cadastrada."
        return (
                f"Nome: {self.nome} | Cargo: {self.cargo} | E-mail: {self.email} | "
                f"Telefone: {self.telefone} | Data Admissao: {self.data_admissao} | Projeto: {self.projeto} | "
                f"Senha: {senha_oculta}"
        )

    def para_dicionario(self):
        return {""
                "nome": self.nome,
                "cargo": self.cargo,
                "email": self.email,
                "telefone": self.telefone,
                "data_admissao": self.data_admissao,
                "projeto": self.projeto

        }

class GerenciadorPessoas:
        def __init__(self):
            self.pessoas = []

        # 1 CRIANDO (adicionar pessoas)

        def adicionar(self, pessoa):
            self.pessoas.append(pessoa)
            print(f"Pessoa '{pessoa.nome}' Adicionada com sucesso ")

        # 2 read listando tudo

        def listar_todas(self):
            if not self.pessoas:
                print("Nenhum Pessoa Cadastrada")
                return

            print("\n-- LISTA COMPLETA DE PESSOAS--")
            for pessoa in self.pessoas:
                print(pessoa.exibir_dados())

        def cadastrar_interativo(self):
            print("\n --- NOVO CADASTRO DE PESSOA ---\n")
            nome = input("Digite o nome completo: ")
            cargo = input("Digite o cargo: ")
            email = input("Digite o e-mail: ")
            telefone = input("Digite o telefone: ")
            data_admissao = input("Digite o data de admissao: ")
            projeto = input("Digite o nome do projeto: ")
            senha = input("Digite uma senha: ")

            #instancia e adiciona automaticamente nan memoria
            nova_pessoa = Pessoa(nome, cargo, email, telefone, data_admissao,projeto, senha)
            self.adicionar(nova_pessoa)


        # 3 buscando pessoas

        def buscar_nome(self, termo):
            """ Busca o nome da pessoa """
            encontrados = [p for p in self.pessoas if termo.lower() in p.nome.lower()]
            return encontrados


        # 4 FILTRANDO (POR PROJETO)

        def filtrar_por_projeto(self, nome_projeto):
            """ Filtra os projetos da pessoa """
            encontrados = [p for p in self.pessoas if p.projeto.lower() == nome_projeto.lower()]
            return encontrados

        # 5 removendo

        def remover_por_email(self, email_projeto):
            """ Remover email da pessoa """
            for pessoa in self.pessoas:
                if pessoa.email.lower() == email_projeto.lower():
                    self.pessoas.remove(pessoa)
                    print(f"Pessoa com e-mail '{email_projeto}' removido com sucesso ")
                    return True
            print(f" Nenhuma pessoa encontrada com o e-mail '{email_projeto}'.")
            return False









