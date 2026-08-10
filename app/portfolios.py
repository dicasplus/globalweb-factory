class Chamado:
    """Classe responsavel por estruturar e formatar solicitaçao final"""

    def __init__(self, projeto, categoria, solicitante, descricao_curta, detalhes):
        self.projeto = projeto
        self.categoria = categoria
        self.solicitante = solicitante
        self.descricao_curta = descricao_curta
        self.detalhes = detalhes # Dicionarios com respostas especificas (exemplo, IP: Patrimonio)

    def gerar_script_detalhado(self):

        """Gera o texto padronizado e formatado pronto para colar no sistema de tickets"""
        script = f"""
    ===========================================================================
                SOLICITAÇÃO DE SUPORTE - {self.projeto.upper()}
    ===========================================================================
    [INFORMAÇÕES GERAIS]
    > Projeto / Contrato : {self.projeto}
    > Categoria : {self.categoria}
    > Solicitante : {self.solicitante}
    > Resumo da Demanda: {self.descricao_curta}
    
    [DETALHAMENTO TÉCNICO]
    """
        for chave, valor in enumerate(self.detalhes):
            script += f".{chave:<20}: {valor}\n"

        script += """==========================================================
        [STATUS]: Aguardando atendimento / triagem
        =================================================
        """
        return script

class GerenciadorPortfolios:
    """ Gerencia os Projetos  / contratanntes e os Fluxos de aberturas de Chamados"""
    def __init__(self):
        #Mapeamento simples de projetos e categorias de suporte disponivel
        self.projeto_categoria = {
            "MCTI": ['Suporte e Sistema / Wiki', 'Acesso a Rede  / VPN', 'Equipamento / Patrimônio'],
            "MEC": ["Analise de Dados", "Liberação de Perfil", "Instalacao de Software"],
            "COPASA": ["Atendimento de Tickets", "Manutenação de Perfil", "Geral" ],
            "Global Web":["Duvidas RH / Ponto", "Suporte interno" ]
        }
    def listar_projetos(self):
        """Exibe todos os projetos disponiveis"""
        print("\n --- PROJETOS  / PORTFOLIOS DISPONÍVEIS ---")
        for idx, proj in enumerate(self.projeto_categoria.keys(), 1):
            print(f" PROJETO {idx}.  {proj} ")
            