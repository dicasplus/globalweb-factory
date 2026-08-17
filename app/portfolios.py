"""Módulo de Gestão de Portfólios, Chamados e Agente de IA para Triagem Automática - GW Factory."""


class Chamado:
    """Estrutura e formata a solicitação final de atendimento."""

    def __init__(
        self,
        projeto,
        categoria,
        subcategoria,
        solicitante,
        resumo,
        detalhes_adicionais=None,
    ):
        self.projeto = projeto
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.solicitante = solicitante
        self.resumo = resumo
        self.detalhes = detalhes_adicionais or {}

    def gerar_script_detalhado(self):
        """Gera o texto padronizado pronto para registrar no sistema de tickets."""
        script = f"""===========================================================================
                    SOLICITAÇÃO DE SUPORTE - GW FACTORY
===========================================================================
[INFORMAÇÕES GERAIS]
> Contrato / Empresa : {self.projeto}
> Categoria          : {self.categoria}
> Subcategoria       : {self.subcategoria}
> Solicitante        : {self.solicitante}
> Resumo da Demanda  : {self.resumo}

[DETALHAMENTO TÉCNICO]
"""
        for chave, valor in self.detalhes.items():
            if valor:
                script += f"> {chave:<20}: {valor}\n"

        script += """===========================================================================
[STATUS]: Aguardando atendimento / triagem N1
==========================================================================="""
        return script


class GerenciadorPortfolios:
    """Gerencia os Projetos / Contratantes e o Catálogo de Serviços de TI."""

    def __init__(self):
        self.contratos = [
            "MCTI",
            "COPASA",
            "MEC",
            "START CAOA",
            "Globalweb",
            "MPM",
            "OUTROS",
        ]

        self.categorias_tecnicas = {
            "🖥️ Equipamentos & Hardwares": [
                "Substituição / Instalação (EST/Patrimônio)",
                "Manutenção / Diagnóstico de Defeito",
                "Periféricos (Teclado, Mouse, Monitor, Headset, Webcam)",
                "Upgrade de Hardware (RAM / SSD)",
            ],
            "🔑 Acessos & Senhas": [
                "Redefinição / Desbloqueio de Senha",
                "Criação de Novo Usuário / Permissões",
                "Acesso a Pastas / Rede / VPN",
                "Perfis de Acesso em Sistemas Corporativos",
            ],
            "⚙️ Sistemas & Softwares": [
                "Erro / Bug em Aplicação",
                "Instalação de Softwares Homologados",
                "Suporte a Sistemas de Ponto / RH",
                "Lentidão / Falha de Execução",
            ],
            "🌐 Redes & Conectividades": [
                "Lentidão / Instabilidade de Conexão",
                "Problemas de Conexão / Wi-Fi",
                "Bloqueio ou Acesso a Sites",
                "Configuração de IP / Ponto de Rede",
                "VPN / FortiClient / GlobalProtect",
            ],
            "🛠️ Infraestrutura e Servidores": [
                "Acesso a Servidores / Storage",
                "Falha em Máquina Virtual (VM)",
                "Backup / Restauração de Arquivos",
                "Unidade Compartilhada / Mapeamento de Rede",
            ],
        }

    def listar_projetos(self):
        """Exibe todos os contratos disponíveis."""
        print("\n--- PROJETOS / PORTFÓLIOS DISPONÍVEIS ---")
        for idx, proj in enumerate(self.contratos, 1):
            print(f"{idx}. {proj}")


# ==============================================================================
# DICIONÁRIO E AGENTE DE IA DE SUPORTE
# ==============================================================================
VOCABULARIO_SUPORTE = {
    "🔑 Acessos & Senhas": [
        "esqueci a senha",
        "senha expirou",
        "bloqueou a conta",
        "não entra no sistema",
        "deu acesso negado",
        "perdi o token",
        "resetar senha",
        "desbloquear usuário",
        "não me deixa logar",
        "senha inválida",
        "conta travada",
        "meu login pifou",
        "senha errada",
        "esqueci o login",
        "trancou o acesso",
        "perdi o 2fa",
        "mudar senha",
        "trocar senha",
        "permissão negada",
        "sem pasta de acesso",
        "sem permissão no sistema",
        "sem perfil",
        "não consigo logar no pc",
        "active directory",
        "ad",
        "ldap",
        "autenticação",
        "perfil corporativo",
        "sso",
        "single sign-on",
        "troca de credenciais",
        "reset de password",
        "mfa",
        "multi-factor authentication",
        "authenticator",
    ],
    "🖥️ Equipamentos & Hardwares": [
        "computador não liga",
        "tela azul",
        "maquina queimou",
        "impressora engoliu papel",
        "mouse travado",
        "teclado pifou",
        "fio partido",
        "monitor piscando",
        "pc lento",
        "computador travou tudo",
        "fumaça na máquina",
        "não sai som",
        "pc esquentando",
        "barulho estranho na maquina",
        "fonte queimou",
        "impressora presa",
        "papel enganchou",
        "monitor apagado",
        "tela preta",
        "fone sem som",
        "microfone mudo",
        "cabo quebrado",
        "carregador queimou",
        "patrimônio",
        "est",
        "nobreak",
        "desktop",
        "notebook",
        "dockstation",
        "troca de hd",
        "troca de ssd",
        "memória ram",
        "substituição de periférico",
        "dispensador",
        "toner",
        "unidade fusora",
        "placa-mãe",
        "cooler",
    ],
    "🌐 Redes & Conectividades": [
        "internet caiu",
        "sem wifi",
        "vpn caindo toda hora",
        "rede fora do ar",
        "cabo desconectado",
        "sinal fraco",
        "site não carrega",
        "sem rede no andar",
        "wi-fi não conecta",
        "caiu a vpn",
        "cabo de rede solto",
        "sem internet no setor",
        "não abre o site da empresa",
        "rede lenta",
        "conexão instável",
        "ficou caindo",
        "endereço ip",
        "dns",
        "dhcp",
        "gateway",
        "ping alto",
        "perda de pacote",
        "forticlient",
        "globalprotect",
        "cisco anyconnect",
        "switch",
        "patch cord",
        "sub-rede",
        "tráfego de rede",
        "ipconfig",
        "renew ip",
        "flushdns",
        "latência",
    ],
    "⚙️ Sistemas & Softwares": [
        "sistema dando erro",
        "módulo travado",
        "não gera pdf",
        "tela congelou",
        "relatório não baixa",
        "deu erro de tela vermelha",
        "o sistema caiu",
        "botão não funciona",
        "erro doido no sistema",
        "fechou sozinho",
        "deu crash",
        "deu bug",
        "travou no carregamento",
        "rodinha girando infinito",
        "não abre o erp",
        "relatório em branco",
        "não salva a alteração",
        "bug no erp",
        "falha de banco",
        "exceção de código",
        "timeout de requisição",
        "atualização de versão",
        "limpeza de cache",
        "cookies",
        "runtime error",
        "null pointer",
        "erro 500",
        "erro 404",
    ],
    "🛠️ Infraestrutura e Servidores": [
        "pasta da rede sumiu",
        "servidor fora",
        "disco cheio",
        "não salva o arquivo",
        "unidade z sumiu",
        "maquina virtual travada",
        "backup demorando",
        "sumiu tudo da pasta",
        "não consigo acessar o servidor",
        "disco no 100%",
        "pasta compartilhada sumiu",
        "não salva na rede",
        "servidor caiu",
        "storage",
        "servidor de arquivos",
        "smb",
        "nfs",
        "maquina virtual",
        "vm",
        "hypervisor",
        "cluster",
        "backup veeam",
        "provisionamento de espaço",
        "volume lógico",
        "raid",
        "san",
        "nas",
    ],
}


class AgentAI:
    """Agente de Inteligência Artificial para Triagem e Classificação de Chamados."""

    def __init__(self):
        self.vocabulario = VOCABULARIO_SUPORTE

    @staticmethod
    def classificar_chamado(texto, contratos=None, categorias_tecnicas=None):
        """Classifica o chamado com base em regras diretas de suporte."""
        texto_lower = texto.lower().strip()

        # Classificação por Regras Reativas
        if any(
            t in texto_lower
            for t in [
                "internet",
                "internnet",
                "rede",
                "wifi",
                "vpn",
                "lenta",
                "caiu",
                "sem conexao",
                "ip",
            ]
        ):
            cat_vencedora = "🌐 Redes & Conectividades"
            subcat_vencedora = "Lentidão / Instabilidade de Conexão"
        elif any(
            t in texto_lower
            for t in [
                "computador",
                "notebook",
                "pc",
                "maquina",
                "impressora",
                "monitor",
                "equipamento",
                "equipamentno",
            ]
        ):
            cat_vencedora = "🖥️ Equipamentos & Hardwares"
            subcat_vencedora = "Substituição / Instalação (EST/Patrimônio)"
        elif any(
            t in texto_lower
            for t in [
                "senha",
                "acesso",
                "login",
                "bloqueado",
                "pasta de rede",
                "permissao",
            ]
        ):
            cat_vencedora = "🔑 Acessos & Senhas"
            subcat_vencedora = "Redefinição / Desbloqueio de Senha"
        else:
            cat_vencedora = "⚙️ Sistemas & Softwares"
            subcat_vencedora = "Geral"

        if categorias_tecnicas and cat_vencedora in categorias_tecnicas:
            subcats = categorias_tecnicas[cat_vencedora]
            if subcats and subcat_vencedora not in subcats:
                subcat_vencedora = subcats[0]

        contrato_sugerido = contratos[0] if contratos else "MCTI"

        return {
            "contrato": contrato_sugerido,
            "categoria": cat_vencedora,
            "subcategoria": subcat_vencedora,
        }

    @staticmethod
    def polir_descricao(
        texto_bruto, categoria, subcategoria, solicitante="Solicitante"
    ):
        """Reescreve o relato do cliente em um texto técnico e fluido sem marcas brutas."""
        relato_limpo = texto_bruto.strip()

        correcoes = {
            "internnet": "internet",
            "infotma": "informa",
            "solciita": "solicita",
            "equipamentno": "equipamento",
            "desenvolver": "desenvolvedor",
            "nao consegue": "não consegue",
            "copasa": "COPASA",
            "mcti": "MCTI",
            "mec": "MEC",
        }
        for erro, correcao in correcoes.items():
            relato_limpo = relato_limpo.replace(erro, correcao)

        nome_solic = (
            solicitante.split(" (")[0]
            if solicitante and "➕ Digitar" not in solicitante
            else "o(a) colaborador(a)"
        )

        return (
            f"Atendimento solicitado por {nome_solic} referente à categoria"
            f" {categoria} ({subcategoria.lower()}).\n\n"
            f'Relato informado: "{relato_limpo}".\n\n'
            "Ação realizada/orientada: Demanda registrada e encaminhada para a"
            " equipe de suporte responsável para análise técnica e atendimento."
        )