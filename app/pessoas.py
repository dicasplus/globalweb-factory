class Pessoa:
    def __init__(self, nome, cargo, email, telefone, data_admissao, projeto):
        self.nome = nome
        self.cargo = cargo
        self.email = email
        self.telefone = telefone
        self.data_admissao = data_admissao
        self.projeto = projeto

    def exibir_dados(self):
        return (
                f"Nome: {self.nome} | Cargo: {self.cargo} | E-mail: {self.email} | "
                f"Telefone: {self.telefone} | Data Admissao: {self.data_admissao} | Projeto: {self.projeto}"
        )

