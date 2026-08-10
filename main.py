from app.pessoas import Pessoa, GerenciadorPessoas
from app.portfolios import GerenciadorPortfolios


def exibir_menu():
    print('=' * 75)
    print("\nSISTEMA GLOBALWEB FACTORY -GESTAO DE PESSOAS E PROCESSOS")
    print("=" * 75)
    print("1 - Cadastrar nova Pessoa")
    print("2 - Listar todas as Pessoas")
    print("3 - Buscar por nome")
    print("4 - Remover por email")
    print("5 - Listar Projetos / Portfolios")
    print("6 - Abrir chamado de Suporte (Guiado)")
    print("0 - SAIR DO PROGRAMA")
    print("=" * 75)


if __name__ == '__main__':

    pessoa1 = Pessoa(
        nome="Charles Ferreira de Moura",
        cargo="Desenvolvedor Junior",
        email="charles@empresa.com",
        telefone="61 9999-9999",
        data_admissao="01/08/2024",
        projeto="MCTI",
        senha="123456"

    )

    pessoa2 = Pessoa(
        nome="Ana Carolina",
        cargo="Analista de Dados",
        email="ana@colabaradores.empresa.com",
        telefone="61 9991-1234",
        data_admissao="01/01/2026",
        projeto="MEC",
        senha="1234567"
    )

    pessoa3 = Pessoa(
        nome="João Milton Alves de Moura",
        cargo="Gerente de RH",
        email="joao@empresa.com",
        telefone="73  98123-4567",
        data_admissao="01/08/2000",
        projeto="Global Web",
        senha="12345678"

    )

    pessoa4 = Pessoa(
        nome="OPERADOR TECNICO",
        cargo="SUPORTE",
        email="suporte@empresa.com",
        telefone="61 9888-7777",
        data_admissao="01/01/2026",
        projeto="Global Web",
        senha="123456789"


    )

    # instanciando e alimentando o gerenciador ---

gerenciador = GerenciadorPessoas()
gerenciador.adicionar(pessoa1)
gerenciador.adicionar(pessoa2)
gerenciador.adicionar(pessoa3)
gerenciador.adicionar(pessoa4)

#Intanciando o Gerador de Portfolios
gerenciador_portfolios = GerenciadorPortfolios()6

# gerenciador.cadastrar_interativo()
while True:
    exibir_menu()
    opcao = input('Escolha uma opção: ').strip().upper()
    if opcao == '1':
        gerenciador.cadastrar_interativo()
    elif opcao == '2':
        gerenciador.listar_todas()
    elif opcao == '3':
        termo = input("Digite o nome para buscar: ")
        resultados = gerenciador.buscar_nome(termo)
        if resultados:
            print(f'\n --Resultados ({len(resultados)}) --- ')
            for p in resultados:
                print(p.exibir_dados())
        else:
            print("Nenhum resultado encontrado")
    elif opcao == '4':
        email = input("Digite o email: ")
        gerenciador.remover_por_email(email)

    elif opcao == '5':
        gerenciador_portfolios.listar_projetos()

    elif opcao == '6':
        solicitante = input("Digite o nome do solicitante: ")
        chamado = gerenciador_portfolios.criar_chamado_guiado(solicitante)
        if chamado:
            print("\n --- SCRIPT GERADO PARA O TICKET---")
            print(chamado.gerar_script_detalhado())
    elif opcao == '0':
        print("Saindo do programa")
        break
    else:
        print("OPÇÃO INVALIDA, DIGITE UM NUMERO DE 0 A 6. ")
