from app.pessoas import Pessoa, GerenciadorPessoas

if __name__ == '__main__':
    pessoa1 = Pessoa(
        nome="Charles Ferreira de Moura",
        cargo="Desenvolvedor Junior",
        email="charles@empresa.com",
        telefone="61 9999-9999",
        data_admissao="01/08/2024",
        projeto="MCTI"
    )

    pessoa2 = Pessoa(
        nome="Ana Carolina",
        cargo="Analista de Dados",
        email="ana@colabaradores.empresa.com",
        telefone="61 9991-1234",
        data_admissao="01/01/2026",
        projeto="MEC"
    )

    pessoa3 = Pessoa(
        nome="João Milton Alves de Moura",
        cargo="Gerente de RH",
        email="joao@empresa.com",
        telefone="73  98123-4567",
        data_admissao="01/08/2000",
        projeto="Global Web"

    )

    pessoa4 = Pessoa(
        nome="OPERADOR TECNICO",
        cargo="SUPORTE",
        email="suporte@empresa.com",
        telefone="61 9888-7777",
        data_admissao="01/01/2026",
        projeto="Global Web"


    )

    # instanciando e alimentando o gerenciador ---

gerenciador = GerenciadorPessoas()
gerenciador.adicionar(pessoa1)
gerenciador.adicionar(pessoa2)
gerenciador.adicionar(pessoa3)
gerenciador.adicionar(pessoa4)


#BUSCAR POR NOME

print("\n --- TESTE 1: BUSCANDO POR NOME ('Moura') --- \n ")
buscar_nome = gerenciador.buscar_nome("Moura")
for p in buscar_nome:
    print(p.exibir_dados())

#filtar por projeto

print("\n ---TESTE 2: FILTRANDO POR PROJETO (Global Web') --- \n")
busca_projeto = gerenciador.filtrar_por_projeto("Global Web")
for p in busca_projeto:
    print(p.exibir_dados())

#remover

print("\n --- Teste 3: removendo por e-mail (' ') --- \n ")
gerenciador.remover_por_email("ana@colabaradores.empresa.com")





# lista completa
print("\n###Cadastro de Pessoas ###")
print('=== LISTA ATUALIZADA APÓS REMOÇAO ===')
gerenciador.listar_todas()

