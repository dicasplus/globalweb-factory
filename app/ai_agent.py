"""Módulo do Agente de Inteligência Artificial do GlobalWeb Factory.

Gerencia classificação de chamados, polimento de texto e triagem reativa.
"""

import importlib
import json
import os
from typing import Any, Dict, List, Optional
import streamlit as st


def _obter_chave_configurada() -> Optional[str]:
    """Obtém a chave da API do Gemini via st.secrets ou variável de ambiente."""
    try:
        chave = st.secrets.get("GEMINI_API_KEY")
        if chave:
            return str(chave)
    except (AttributeError, KeyError, FileNotFoundError):
        pass
    return os.getenv("GEMINI_API_KEY")


class AgenteAtendimento:
    """Agente de Inteligência Artificial para classificação, polimento
    e análise de governança de chamados no GlobalWeb Factory.
    """

    def __init__(self, chave_api: Optional[str] = None):
        self.api_key: Optional[str] = chave_api or _obter_chave_configurada()
        self.model: Any = None

        if self.api_key:
            try:
                genai = importlib.import_module("google.generativeai")
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
            except (ImportError, Exception) as e:
                print(f"Aviso: Modo reativo ativo (API Gemini desativada): {e}")

    def classificar_chamado(
        self,
        texto_usuario: str,
        contratos: List[str],
        categorias_tecnicas: Dict[str, List[str]],
    ) -> Dict[str, Any]:
        """Analisa a descrição do usuário e sugere Contrato, Categoria,
        Subcategoria e Impacto.
        """
        if not texto_usuario.strip():
            return {}

        # 1. Consulta ao Modelo Gemini (caso a chave esteja configurada)
        if self.model is not None:
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
                    res_text = res_text[7:]
                    if res_text.endswith("```"):
                        res_text = res_text[:-3]
                    res_text = res_text.strip()
                elif res_text.startswith("```"):
                    res_text = res_text[3:]
                    if res_text.endswith("```"):
                        res_text = res_text[:-3]
                    res_text = res_text.strip()

                dados_json = json.loads(res_text)
                if isinstance(dados_json, dict):
                    return dados_json
            except Exception as e:
                print(f"Erro na chamada da IA para classificação: {e}")

        # 2. Fallback Inteligente Reativo por Palavras-Chave
        texto_lc = texto_usuario.lower().strip()

        contrato_sugerido = contratos[0] if contratos else "MCTI"
        for contrato in contratos:
            if contrato.lower() in texto_lc:
                contrato_sugerido = contrato
                break

        mapeamento_palavras = {
            "Acessos": [
                "senha",
                "palavra passe",
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
                "credencial",
            ],
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
                "toner",
                "equipamento",
                "equipamentno",
            ],
            "Redes": [
                "internet",
                "internnet",
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
            ],
        }

        categoria_sugerida = (
            list(categorias_tecnicas.keys())[0]
            if categorias_tecnicas
            else "Sistemas & Softwares"
        )

        palavras_texto = texto_lc.split()
        cat_encontrada = False

        for termo_chave, palavras in mapeamento_palavras.items():
            chave_real_sistema = None
            for cat_real in categorias_tecnicas.keys():
                if termo_chave.lower() in cat_real.lower():
                    chave_real_sistema = cat_real
                    break

            if chave_real_sistema:
                for palavra in palavras:
                    if palavra in palavras_texto or (
                        len(palavra) > 2 and palavra in texto_lc
                    ):
                        categoria_sugerida = chave_real_sistema
                        cat_encontrada = True
                        break

            if cat_encontrada:
                break

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
            "justificativa": (
                f"Classificado na categoria '{categoria_sugerida}'"
                f" ({subcat_sugerida})."
            ),
        }

    def polir_descricao(
        self,
        texto_bruto: str,
        categoria: str = "",
        subcategoria: str = "",
        solicitante: str = "",
    ) -> str:
        """Pega o relato do usuário e o reescreve em um texto fluido, elegante e profissional."""
        if not texto_bruto.strip():
            return ""

        # 1. Reescrita Narrativa via Gemini
        if self.model is not None:
            prompt = f"""
            Você é um analista de Service Desk de TI.
            Reescreva a solicitação abaixo em forma de texto narrativo curto, fluido e profissional (SEM marcadores como [RESUMO], SEM caixas de seleção, SEM listas ou código Markdown rígido).

            Solicitante: {solicitante}
            Categoria: {categoria}
            Subcategoria: {subcategoria}
            Relato do Usuário: "{texto_bruto}"

            Exemplo de tom de resposta esperado:
            "Atendimento registrado para o(a) colaborador(a) referente a [subcategoria]. O solicitante entrou em contato informando [relato reescrito com correção ortográfica]. Demanda encaminhada para a equipe responsável para tratativa técnica."
            """
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"Erro ao polir texto com IA: {e}")

        # 2. Fallback Narrativo
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

        subcat_txt = subcategoria.lower() if subcategoria else "suporte técnico"

        return (
            f"Atendimento solicitado por {nome_solic} referente a {subcat_txt}.\n\n"
            f'Relato informado: "{relato_limpo}".\n\n'
            "Ação realizada/orientada: Demanda registrada e encaminhada para a"
            " equipe de suporte responsável para análise técnica e atendimento."
        )