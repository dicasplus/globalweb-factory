import json
import os


class AgenteAtendimento:
    """Agente de Inteligência Artificial para classificação, polimento
    e análise de governança de chamados no GlobalWeb Factory.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = None

        # Tenta inicializar a biblioteca do Gemini se a chave estiver configurada
        if self.api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception as e:
                print(f"Aviso: Não foi possível carregar a API do Gemini: {e}")

    def classificar_chamado(
        self, texto_usuario: str, contratos: list, categorias_tecnicas: dict
    ) -> dict:
        """Analisa a descrição do usuário e sugere Contrato, Categoria,
        Subcategoria e Impacto.
        """
        if not texto_usuario.strip():
            return {}

        # 1. Se houver chave e modelo configurado, consulta o Gemini
        if self.model:
            prompt = f"""
            Você é um especialista em Service Desk e triagem de chamados de TI.
            Dada a seguinte solicitação do usuário:
            "{texto_usuario}"

            Selecione a melhor opção para cada campo com base nestas listas permitidas:
            - Contratos disponíveis: {json.dumps(contratos)}
            - Categorias e Subcategorias técnicas disponíveis: {json.dumps(categorias_tecnicas)}

            Responda EXCLUSIVAMENTE em formato JSON com a seguinte estrutura:
            {{
                "contrato": "nome do contrato selecionado",
                "categoria": "nome da categoria selecionada",
                "subcategoria": "nome da subcategoria selecionada",
                "impacto": "Baixo" | "Médio" | "Alto",
                "justificativa": "breve explicação do motivo da escolha"
            }}
            """
            try:
                response = self.model.generate_content(prompt)
                res_text = response.text.strip()

                if res_text.startswith("```json"):
                    res_text = res_text[7:-3].strip()
                elif res_text.startswith("```"):
                    res_text = res_text[3:-3].strip()

                return json.loads(res_text)
            except Exception as e:
                print(f"Erro na chamada da IA para classificação: {e}")

        # 2. Fallback Inteligente Expandido por Palavras-Chave
        texto_lc = texto_usuario.lower()

        # 🏢 A. Identifica o Contrato
        contrato_sugerido = contratos[0] if contratos else "MCTI"
        for contrato in contratos:
            if contrato.lower() in texto_lc:
                contrato_sugerido = contrato
                break

        # 📁 B. Dicionário Amplo com Prioridade Corrigida para Categorias
        mapeamento_palavras = {
            # 🔑 1º LUGAR: Acessos & Senhas (Prioridade máxima para gestão de credenciais)
            "Acessos": [
                "senha",
                "palavra passe",
                "palavra-passe",
                "acesso",
                "login",
                "desbloqueio",
                "usuario",
                "permissao",
                "reset",
                "redefinir",
                "mfa",
                "2fa",
                "esqueci",
                "troca de senha",
                "mudar a senha",
                "credencial",
            ],
            # ⚙️ 2º LUGAR: Sistemas & Softwares
            "Sistemas": [
                "rh",
                "folha",
                "sei",
                "sap",
                "siga",
                "sistema",
                "software",
                "erro no sistema",
                "banco de dados",
                "office",
                "excel",
                "word",
                "outlook",
                "teams",
                "glpi",
                "bug",
            ],
            # 🖥️ 3º LUGAR: Equipamentos & Hardwares
            "Equipamentos": [
                "impressora",
                "monitor",
                "teclado",
                "mouse",
                "hardware",
                "computador",
                "pc",
                "notebook",
                "est",
                "patrimonio",
                "headset",
                "webcam",
                "fonte",
                "cabo hdmi",
                "toner",
                "papel preso",
                "gabinete",
            ],
            # 🌐 4º LUGAR: Redes & Conectividades
            "Redes": [
                "internet",
                "wifi",
                "wi-fi",
                "vpn",
                "rede",
                "cabo",
                "dns",
                "ip",
                "sem conexao",
                "lento",
                "queda",
                "sinal",
                "roteador",
                "switch",
            ],
        }

        # Define Categoria padrão
        categoria_sugerida = (
            list(categorias_tecnicas.keys())[0]
            if categorias_tecnicas
            else "Sistemas & Softwares"
        )

        palavras_texto = texto_lc.split()

        # Procura correspondência ignorando emojis e formatação
        cat_encontrada = False
        for termo_chave, palavras in mapeamento_palavras.items():
            # Busca qual é a chave REAL cadastrada no sistema que contém esse termo
            chave_real_sistema = None
            for cat_real in categorias_tecnicas.keys():
                if termo_chave.lower() in cat_real.lower():
                    chave_real_sistema = cat_real
                    break

            if chave_real_sistema:
                for palavra in palavras:
                    # Confere palavra isolada ou trecho
                    if palavra in palavras_texto or (
                        len(palavra) > 2 and palavra in texto_lc
                    ):
                        categoria_sugerida = chave_real_sistema
                        cat_encontrada = True
                        break

            if cat_encontrada:
                break

        # 📄 C. Seleciona a Subcategoria mais adequada
        subcats_disponiveis = categorias_tecnicas.get(
            categoria_sugerida, ["Outros"]
        )
        subcat_sugerida = subcats_disponiveis[0]

        for sub in subcats_disponiveis:
            sub_lc = sub.lower()
            palavras_sub = [
                p
                for p in sub_lc.replace("/", " ")
                .replace("(", " ")
                .replace(")", " ")
                .split()
                if len(p) > 3
            ]
            if any(p in texto_lc for p in palavras_sub):
                subcat_sugerida = sub
                break

        # ⚡ D. Identifica o Impacto
        impacto_sugerido = "Baixo"
        if any(
            w in texto_lc
            for w in [
                "parou",
                "urgente",
                "sem sistema",
                "critico",
                "fora do ar",
                "parado",
                "emergencia",
                "trava",
            ]
        ):
            impacto_sugerido = "Alto"
        elif any(
            w in texto_lc
            for w in ["lento", "falha", "erro", "bug", "problema", "oscilando"]
        ):
            impacto_sugerido = "Médio"

        return {
            "contrato": contrato_sugerido,
            "categoria": categoria_sugerida,
            "subcategoria": subcat_sugerida,
            "impacto": impacto_sugerido,
            "justificativa": f"Identificado palavra-chave associada ao contrato '{contrato_sugerido}' e categoria '{categoria_sugerida}'.",
        }

    def polir_descricao(
        self, texto_bruto: str, categoria: str = "", subcategoria: str = ""
    ) -> str:
        """Pega o relato inicial do usuário e o padroniza em uma ordem de serviço
        técnica detalhada com checklist para suporte N1/N2.
        """
        if not texto_bruto.strip():
            return ""

        # 1. Se a chave da API do Gemini estiver configurada
        if self.model:
            prompt = f"""
            Você é um analista de Service Desk especialista em documentação de incidentes e requisições de TI.
            Reescreva e padronize a solicitação abaixo para que fique extremamente clara e técnica para a equipe de atendimento.

            Solicitação Bruta: "{texto_bruto}"
            Categoria: {categoria}
            Subcategoria: {subcategoria}

            Gere a resposta no seguinte formato estruturado (use Markdown):

            **[RESUMO EXECUTIVO]**
            (Breve resumo do problema)

            **[DETALHAMENTO TÉCNICO]**
            (Descrição clara da demanda)

            **[CHECKLIST DE DIAGNÓSTICO PARA N1/N2]**
            - [ ] Validar identificação e permissões do usuário
            - [ ] Verificar conectividade/status do equipamento ou serviço
            - [ ] Confirmar se o problema ocorre em outro dispositivo/ambiente
            - [ ] Registrar logs/prints do erro no chamado
            """
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"Erro ao polir texto com IA: {e}")

        # 2. Fallback Inteligente (sem API Key)
        return (
            f"**[RESUMO EXECUTIVO]**\n"
            f"Solicitação referente a {categoria} ({subcategoria}).\n\n"
            f"**[DETALHAMENTO TÉCNICO]**\n"
            f"{texto_bruto.capitalize()}.\n\n"
            f"**[CHECKLIST DE DIAGNÓSTICO PARA N1/N2]**\n"
            f"- [ ] Validar cadastro e permissões do usuário solicitante\n"
            f"- [ ] Verificar status de conectividade/rede\n"
            f"- [ ] Testar reprodutibilidade do comportamento relatado\n"
            f"- [ ] Coletar evidências/prints do erro"
        )