class Chamado:
    """Classe responsavel por estruturar e formatar solicitaçao final"""

    def __init__(self, projeto, categoria, subcategoria, solicitante, resumo, detalhes_adicionais):
        self.projeto = projeto
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.solicitante = solicitante
        self.resumo = resumo,
        self.detalhes = detalhes_adicionais # Dicionarios com respostas especificas (exemplo, IP: Patrimonio)

    def gerar_script_detalhado(self):

        """Gera o texto padronizado e formatado pronto para colar no sistema de tickets"""
        script = f"""
    ===========================================================================
                SOLICITAÇÃO DE SUPORTE - GW FACTORY
    ===========================================================================
    [INFORMAÇÕES GERAIS]
    > Contrato / Empresa : {self.projeto}
    > Categoria : {self.categoria}
    > Subcategoria : {self.subcategoria}
    > Solicitante : {self.solicitante}
    > Resumo da Demanda: {self.resumo}
    
    [DETALHAMENTO TÉCNICO]
    """
        for chave, valor in self.detalhes.items():
            if valor:
                script += f">{chave:<20}: {valor}\n"
                script += """==========================================================
                            [STATUS]: Aguardando atendimento / triagem
                            =================================================
                                                                            """
                return script

class GerenciadorPortfolios:
    """ Gerencia os Projetos  / contratanntes e os Fluxos de aberturas de Chamados"""
    def __init__(self):
        #Mapeamento simples de projetos e categorias de suporte disponivel
        self.contratos = [
            #lista simples e expansível de contratos
            "MCTI",
            "COPASA",
            "Global Web",
            "MEC",
            "MPM",
            "START CAOA",
            "OUTROS"
        ]

        #Categorias e subcategorias
        self.categorias_tecnicas = {

            "🖥️ Equipamentos & Hardawares" :[
                "Substituição / Instalação (EST/Patrimônio)",
                "Manutenção / Diagnóstico de Defeito",
                "Periféricos (Teclado, Mouse, Monitor, Headset, webcam)"

            ],

            "🔑 Acessos & Senhas":[

                "Redefinição /Desbloqueio de senha",
                "Criação de Novo Usuário / Permissões",
                "Acesso a Pastas / Rede / VPN"
            ],
            "⚙️ Sistemas & Softwares":[
                "Erro / Bug em aplicaçã",
                "instalação de Software Homologados",
                "Suporte a Sistemas de Ponto /RH"

            ],

            "🌐 Redes & Conectividades": [
                "Problemas de Conexão / Wi-fi",
                "Bloqueio ou acesso para Sites",
                "Configuração de IP / Ponto de Rede",
                "lentidão na Rede "

            ]

        }


    def listar_projetos(self):
        """Exibe todos os projetos disponiveis"""
        print("\n --- PROJETOS  / PORTFOLIOS DISPONÍVEIS ---")
        for idx, proj in enumerate(self.projeto_categoria.keys(), 1):
            print(f" PROJETO {idx}.  {proj} ")

    def criar_chamado_guiado(self, nome_solicitante):
        """Passo a passo interativo para gerar a descrição detalhada do chamado"""
        print("\n --- Abertura DE CHAMADO RÁPIDO / SOLICITAÇÃO")

        # 1 - Seleção do projeto

        projeto = list(self.projeto_categoria.keys())
        for idx, proj in enumerate(projeto, 1):
            print(f"{idx} - {proj} ")

        opcao_proj = input("\n Escolha o numero do projeto / Contrato:").strip()
        if not opcao_proj.isdigit() or int(opcao_proj) < 1 or int(opcao_proj) > len(projeto):
            print("Opção de Projeto Inválida")
            return None

        projeto_escolhido = projeto[int(opcao_proj) -1]

        # 2 Seleção da Categoria

        categorias = self.projeto_categoria[projeto_escolhido]
        print("\nCategorias para {projeto_escolhido}:")
        for idx, cat in enumerate(categorias, 1):
            print(f"{idx} - {cat} ")

        opcao_cat = input("\nEscolha a categoria da necessidade: ").strip()
        if not opcao_cat.isdigit() or int(opcao_cat) > len(categorias):
            print("Opção de categoria inválida")
            return None

        categoria_escolhida = categorias[int(opcao_cat) -1]

        # 3 - Pergunta Geral
        resumo = input("\nDigite um resumo curto da necessidade:")

        # 4 - Perguntas automaticas / específicas de acordo com o que foi escolhido

        detalhes_tecnicos = {}
        print("\n --- Preencha as informações específicas ---")

        if "Equipamento" in categoria_escolhida or "Patrimônio:  " in categoria_escolhida:
            detalhes_tecnicos["Código Patrimônio (EST)"] = input("Número do Patrimônio/EST do Equipamento:")
            detalhes_tecnicos["Localização / Andar "] = input("Andar / Sala: ")
            detalhes_tecnicos["IP do Host"] = input("Endereço IP (se souber): ")
        elif "Acesso" in categoria_escolhida or "Perfil" in categoria_escolhida:
            detalhes_tecnicos["Sistemas afetados"] = input("Nome do Sistema / Serviço")
            detalhes_tecnicos["Nivel de Persmissão"] = input("Nível de acesso necessário:")
            detalhes_tecnicos["Justificativa"] = input("Motivo do acesso")
        else:
            detalhes_tecnicos["Decrição do Problema"] = input("Detalhe do ocorrido: ")
            detalhes_tecnicos["Impacto no trabalho"] = input("Impacto (Baixo / Médio / Crítico):  ")

        # 5 instancia o chamado e gera o script final

        novo_chamado = Chamado(
            projeto = projeto_escolhido,
            categoria = categoria_escolhida,
            solicitante= nome_solicitante,
            descricao_curta= resumo,
            detalhes= detalhes_tecnicos

        )

        return novo_chamado







