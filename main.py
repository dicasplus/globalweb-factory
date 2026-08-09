from app.pessoas import Pessoa

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

    print("### CADASTRO DE PESSOAS ###")
    print(pessoa1.exibir_dados())
    print(pessoa2.exibir_dados())
    print(pessoa3.exibir_dados())
    print(pessoa4.exibir_dados())

    lista_pessoas = [pessoa1, pessoa2, pessoa3, pessoa4]

    print(f"\ntotal de Pessoas na memoria: {len(lista_pessoas)}")


