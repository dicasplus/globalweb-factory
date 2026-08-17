"""Módulo de Geração de Relatórios e Exportação (Excel & PDF).

Centraliza a lógica de relatórios inteligentes para os gestores da GlobalWeb Factory.
"""

from io import BytesIO
from typing import Any, Dict, List
import pandas as pd


class GerenciadorRelatorios:
    """Responsável por processar dados, exportar para Excel e gerar relatórios executivos."""

    @staticmethod
    def converter_para_excel(dados: List[Dict[str, Any]]) -> bytes:
        """Converte uma lista de dicionários (chamados) em um arquivo Excel formatado (Bytes)."""
        df = pd.DataFrame(dados)
        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Relatório Chamados')

        return output.getvalue()

    @staticmethod
    def filtrar_dados_por_ia(prompt: str, chamados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filtra os chamados com base no comando em texto livre do gestor."""
        prompt_lower = str(prompt or "").lower()
        filtrados = []

        for c in chamados:
            match = True
            impacto_val = str(c.get("impacto") or "")
            status_val = str(c.get("status") or "").lower()
            projeto_val = str(c.get("projeto") or "").lower()

            if "crítico" in prompt_lower and impacto_val not in ["Crítico / Alta", "Alto"]:
                match = False
            if "aberto" in prompt_lower and status_val != "aberto":
                match = False
            if "mcti" in prompt_lower and "mcti" not in projeto_val:
                match = False
            if "copasa" in prompt_lower and "copasa" not in projeto_val:
                match = False
            if "mec" in prompt_lower and "mec" not in projeto_val:
                match = False

            if match or not prompt_lower.strip():
                filtrados.append(c)

        return filtrados if filtrados else chamados

    @staticmethod
    def obter_insights_executivos(dados: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Gera métricas e insights automáticos para o painel gerencial."""
        if not dados:
            return {"total": 0, "criticos": 0, "status_predominante": "N/A", "projeto_frequente": "N/A"}

        total = len(dados)
        criticos = sum(1 for c in dados if str(c.get("impacto")) in ["Crítico / Alta", "Alto"])

        status_lista = [str(c.get("status") or "Aberto") for c in dados]
        status_predominante = max(set(status_lista), key=status_lista.count) if status_lista else "N/A"

        projetos_lista = [str(c.get("projeto") or "Geral") for c in dados]
        projeto_frequente = max(set(projetos_lista), key=projetos_lista.count) if projetos_lista else "N/A"

        return {
            "total": total,
            "criticos": criticos,
            "status_predominante": status_predominante,
            "projeto_frequente": projeto_frequente
        }