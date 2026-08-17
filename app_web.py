"""Aplicação Web Principal - GlobalWeb Factory.

Gerencia autenticação, controle de perfil (RBAC), navegação e abertura de
chamados.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

from app.ai_agent import AgenteAtendimento
from app.database import DatabaseManager
from app.pessoas import GerenciadorPessoas, Pessoa
from app.portfolios import GerenciadorPortfolios
from app.reports import GerenciadorRelatorios


# ==============================================================================
# FUNÇÃO DE CONTROLE DE PERMISSÕES (RBAC)
# ==============================================================================
def obter_nivel_permissao() -> str:
    """Retorna o nível de acesso do usuário logado: 'admin', 'supervisor' ou 'operador'."""
    usuario_atual = st.session_state.get("usuario_logado")
    if not usuario_atual or not isinstance(usuario_atual, dict):
        return "visitante"

    cargo = str(usuario_atual.get("cargo") or "").lower()

    if any(
            p in cargo
            for p in ["gestor", "gerente", "diretor", "dev", "admin", "teste"]
    ):
        return "admin"
    elif any(p in cargo for p in ["supervisor", "coordenador", "lider"]):
        return "supervisor"
    else:
        return "operador"


# ==============================================================================
# CONFIGURAÇÕES INICIAIS DA APLICAÇÃO
# ==============================================================================
st.set_page_config(
    page_title="GLOBAL WEB FACTORY", page_icon=":robot_face:", layout="wide"
)


# Definição da janela modal para pré-visualização de chamados
@st.dialog("📋 Detalhes Completos do Chamado", width="large")
def modal_detalhes_chamado(chamado):
    st.write(f"**Protocolo:** {chamado.get('protocolo', 'N/D')}")

    col_modal1, col_modal2 = st.columns(2)
    with col_modal1:
        st.text(f"Solicitante: {chamado.get('solicitante', 'N/D')}")
        st.text(f"Contrato: {chamado.get('contrato', 'N/D')}")
    with col_modal2:
        st.text(f"Categoria: {chamado.get('categoria', 'N/D')}")
        st.text(f"Impacto: {chamado.get('impacto', 'N/D')}")

    st.markdown("---")
    st.text_area(
        "Resumo / Descrição Detalhada",
        value=chamado.get('resumo', 'Sem descrição informada.'),
        disabled=True,
        height=150
    )

    if st.button("Fechar Janela", type="primary", use_container_width=True):
        st.rerun()


# Inicialização garantida do Menu e Estados
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "menu_selecionado" not in st.session_state:
    st.session_state.menu_selecionado = "🏠 Início"

# Redirecionamento por Perfil de Acesso
if st.session_state.usuario_logado is not None:
    nivel_atual = obter_nivel_permissao()
    if nivel_atual == "operador" and "redirecionado" not in st.session_state:
        st.session_state.menu_selecionado = "🎫 Abertura de Chamado"
        st.session_state.redirecionado = True

# Inicialização dos Gerenciadores de Banco e Classes
if "db" not in st.session_state:
    st.session_state.db = DatabaseManager()

if "gerenciador" not in st.session_state:
    st.session_state["gerenciador"] = GerenciadorPessoas()
    p1 = Pessoa(
        "Charles Ferreira de Moura",
        "Dev Junior",
        "charles@empresa.com",
        "61 9999-9999",
        "01/08/2024",
        "MCTI, COPASA",
        "123456",
    )
    p2 = Pessoa(
        "Ana Carolina",
        "Analista de Dados",
        "ana@colaboradores.empresa.com",
        "61 9991-1234",
        "01/01/2026",
        "MEC",
        "1234567",
    )
    st.session_state.gerenciador.adicionar(p1)
    st.session_state.gerenciador.adicionar(p2)

if "gerenciador_portfolios" not in st.session_state:
    st.session_state.gerenciador_portfolios = GerenciadorPortfolios()

if "agent_ai" not in st.session_state:
    st.session_state.agent_ai = AgenteAtendimento()

gerenciador_port: GerenciadorPortfolios = st.session_state.gerenciador_portfolios
agent_ai: AgenteAtendimento = st.session_state.agent_ai

# ==============================================================================
# MENU DE NAVEGAÇÃO LATERAL
# ==============================================================================
menu: str = str(st.session_state.get("menu_selecionado") or "🏠 Início")

if st.session_state.usuario_logado is not None:
    with st.sidebar:
        st.image("logo.png", use_container_width=True)

        user_info: Dict[str, Any] = st.session_state.usuario_logado
        st.markdown(f"### 👤 {str(user_info.get('nome') or 'Usuário')}")
        st.caption(f"Cargo: {str(user_info.get('cargo') or 'N/A')}")
        st.markdown("---")

        opcoes_menu = [
            "🏠 Início",
            "📋 Listar Pessoas",
            "👤 Cadastrar Pessoa",
            "🎫 Abertura de Chamado",
            "📊 Histórico de Chamados",
            "📊 Relatórios Inteligentes",
            "📁 Projetos / Portfólios"

        ]

        idx_menu = 0
        if st.session_state.menu_selecionado in opcoes_menu:
            idx_menu = opcoes_menu.index(st.session_state.menu_selecionado)

        menu = str(st.radio("Navegação", opcoes_menu, index=idx_menu))
        st.session_state.menu_selecionado = menu

        st.markdown("---")

        if st.button("🚪 Sair da Conta", type="secondary"):
            st.session_state.usuario_logado = None
            st.session_state.menu_selecionado = "🏠 Início"
            st.rerun()

# ------------------------------------------------------------------------------
# TELA 0: INÍCIO
# ------------------------------------------------------------------------------
if menu == "🏠 Início":

    if st.session_state.usuario_logado is not None:
        usr_dados: Dict[str, Any] = st.session_state.usuario_logado

        st.success(f"👋 Bem-vindo(a) de volta, **{str(usr_dados.get('nome') or '')}**!")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("logo.png", use_container_width=True)

        st.markdown(
            "<h1 style='text-align: center;'>GlobalWeb Factory</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color:#888;'>Painel de Controle"
            f" - {str(usr_dados.get('cargo') or '')}</h3>",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        chamados_todos: List[Dict[str, Any]] = st.session_state.db.listar_chamados()

        projetos_disponiveis = [
            "Todos os Contratos",
            "MCTI",
            "COPASA",
            "START CAOA",
            "MEC",
            "Globalweb",
        ]

        col_filtro1, col_filtro2 = st.columns([2, 1])
        with col_filtro1:
            st.subheader("🏢 Visão Geral dos Contratos Integrados")
        with col_filtro2:
            contrato_selecionado = st.selectbox(
                "Filtrar por Cliente/Contrato:", projetos_disponiveis
            )

        if contrato_selecionado != "Todos os Contratos":
            chamados_banco = [
                c
                for c in chamados_todos
                if c.get("projeto") == contrato_selecionado
            ]
        else:
            chamados_banco = chamados_todos

        total_chamados = len(chamados_banco)
        chamados_urgentes = sum(
            1
            for c in chamados_banco
            if c.get("impacto") in ["Crítico / Alta", "Alto"]
        )

        kpi1, kpi2, kpi3 = st.columns(3)

        with kpi1:
            st.metric(
                label="Total de Chamados",
                value=total_chamados,
                delta=str(contrato_selecionado),
            )
        with kpi2:
            st.metric(
                label="Impacto Crítico / Alto",
                value=chamados_urgentes,
                delta_color="inverse",
            )
        with kpi3:
            st.metric(
                label="Status do Contrato",
                value="Operacional",
                delta="Hub Ativo",
            )

        st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            st.info(f"""
                    ### 👤 Seus Dados de Acesso
                    * **E-mail:** {str(usr_dados.get('email') or '')}
                    * **Projetos Atribuídos:** `{str(usr_dados.get('projeto') or '')}`
                    """)

        with c2:
            st.success("""
                    ### 🎫 Atendimento Ativo
                    * Utilize o menu lateral para **Abertura de Chamados**.
                    * Acompanhe os SLAs na aba de **Histórico de Chamados**.
                    """)

        st.markdown("---")

        if st.button("🚪 Sair do Sistema", type="secondary"):
            st.session_state.usuario_logado = None
            st.rerun()

    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("logo.png", use_container_width=True)

        st.markdown(
            "<h1 style='text-align: center;'>GlobalWeb Factory</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color:#888;'>Portal Único de"
            " Gestão e Suporte Integrado</h3>",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        tab_login, tab_cadastro = st.tabs(
            ["🔑 Acessar Minha Conta", "📝 Não tenho cadastro (Cadastrar-me)"]
        )

        with tab_login:
            st.subheader("Autenticação de Colaborador")
            st.caption("Informe seu e-mail e senha cadastrados para acessar.")

            with st.form("form_login_inicio"):
                login_email = st.text_input(
                    "E-mail Corporativo", placeholder="seu.nome@empresa.com"
                )
                login_senha = st.text_input("Senha de Acesso", type="password")

                btn_entrar = st.form_submit_button(
                    "🔑 Entrar no Sistema", type="primary"
                )

                if btn_entrar:
                    colaborador = st.session_state.db.buscar_pessoa_por_login(
                        str(login_email or ""), str(login_senha or "")
                    )

                    if colaborador:
                        st.session_state.usuario_logado = colaborador
                        st.balloons()
                        st.success(
                            f"✅ Bem-vindo(a), **{str(colaborador.get('nome') or '')}**!"
                        )
                        st.rerun()
                    else:
                        st.error(
                            "❌ E-mail ou senha incorretos. Verifique suas"
                            " credenciais ou faça o cadastro."
                        )

        with tab_cadastro:
            st.subheader("Criar Novo Cadastro de Colaborador")
            st.caption(
                "Preencha os dados abaixo para salvar no banco de dados e"
                " liberar o acesso."
            )

            with st.form("form_cadastro_rapido"):
                col_c1, col_c2 = st.columns(2)

                with col_c1:
                    novo_nome = st.text_input("Nome Completo")
                    novo_cargo = st.text_input(
                        "Cargo", placeholder="Ex: Analista de TI"
                    )
                    novo_email = st.text_input("E-mail Corporativo")

                with col_c2:
                    novo_telefone = st.text_input("Telefone / Celular")
                    nova_admissao = st.text_input(
                        "Data de Admissão", placeholder="DD/MM/AAAA"
                    )
                    novos_projetos = st.multiselect(
                        "Projetos de Atuação",
                        [
                            "MCTI",
                            "MEC",
                            "COPASA",
                            "Globalweb",
                            "Start Caoa",
                        ],
                        default=["MCTI"],
                    )
                    nova_senha = st.text_input(
                        "Crie uma Senha de Acesso", type="password"
                    )

                btn_confirmar_cadastro = st.form_submit_button(
                    "✨ Confirmar e Salvar Cadastro"
                )

                if btn_confirmar_cadastro:
                    if (
                            novo_nome
                            and novo_email
                            and nova_senha
                            and novos_projetos
                    ):
                        string_proj = ", ".join(novos_projetos)

                        nova_pessoa_dict = {
                            "nome": novo_nome,
                            "cargo": novo_cargo,
                            "email": novo_email,
                            "telefone": novo_telefone,
                            "data_admissao": nova_admissao,
                            "projeto": string_proj,
                            "senha": nova_senha,
                        }

                        try:
                            st.session_state.db.salvar_pessoa(nova_pessoa_dict)
                            st.session_state.usuario_logado = nova_pessoa_dict
                            st.balloons()
                            st.success(
                                f"🎉 Cadastro de **{novo_nome}** salvo no banco"
                                " com sucesso!"
                            )
                            st.rerun()

                        except Exception as e:
                            st.error(
                                f"⚠️ Erro ao salvar cadastro (este e-mail pode"
                                f" já estar cadastrado): {e}"
                            )
                    else:
                        st.warning(
                            "⚠️ Preencha Nome, E-mail, Senha e escolha pelo"
                            " menos 1 Projeto."
                        )

        st.markdown("---")
        st.caption("🚀 **GlobalWeb Factory** | Desenvolvido por Charles")

# ------------------------------------------------------------------------------
# TELA 1: LISTAGEM DE PESSOAS
# ------------------------------------------------------------------------------
elif menu == "📋 Listar Pessoas":
    st.title("📋 Gestão e Listagem de Colaboradores")
    st.caption(
        "Visualização centralizada da equipe e edição de dados cadastrais."
    )

    pessoas_banco: List[Dict[str, Any]] = st.session_state.db.listar_pessoas()
    nivel_acesso = obter_nivel_permissao()

    if pessoas_banco:
        st.dataframe(
            pessoas_banco,
            use_container_width=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", format="#%d"),
                "nome": "Nome Completo",
                "cargo": "Cargo",
                "email": "E-mail",
                "telefone": "Telefone",
                "data_admissao": "Admissão",
                "projeto": "Contratos Atribuídos",
                "senha": None,
            },
            hide_index=True,
        )

        st.markdown("---")
        st.subheader("✏️ Alterar Cadastro de Colaborador")

        if nivel_acesso == "admin":
            lista_cargos_padrao = [
                "Gestor de TI",
                "Coordenador de Operações",
                "Dev / Analista de Sistemas",
                "Supervisor de Atendimento",
                "Líder Técnico",
                "Analista de Suporte",
                "Operador de Call Center",
                "Técnico de Campo",
            ]

            opcoes_pessoas = {
                f"#{p.get('id')} - {p.get('nome')} ({p.get('cargo')})": p
                for p in pessoas_banco
            }

            pessoa_selecionada_chave = st.selectbox(
                "Selecione o colaborador que deseja editar:",
                options=list(opcoes_pessoas.keys()),
            )

            if pessoa_selecionada_chave:
                pessoa_dados = opcoes_pessoas[pessoa_selecionada_chave]

                cargo_atual = str(pessoa_dados.get("cargo") or "")
                index_cargo = 0
                for idx, c in enumerate(lista_cargos_padrao):
                    if c in cargo_atual:
                        index_cargo = idx
                        break

                with st.form("form_editar_pessoa"):
                    col_e1, col_e2 = st.columns(2)

                    with col_e1:
                        edit_nome = st.text_input(
                            "Nome Completo",
                            value=str(pessoa_dados.get("nome") or ""),
                        )
                        edit_cargo_sel = st.selectbox(
                            "Cargo / Função Corporativa",
                            options=lista_cargos_padrao,
                            index=index_cargo,
                        )
                        edit_cargo_comp = st.text_input(
                            "Especificação da Função (Opcional)",
                            placeholder="Ex: Nível 2 / Noite",
                        )
                        edit_email = st.text_input(
                            "E-mail Corporativo",
                            value=str(pessoa_dados.get("email") or ""),
                        )

                    with col_e2:
                        edit_telefone = st.text_input(
                            "Telefone",
                            value=str(pessoa_dados.get("telefone") or ""),
                        )
                        edit_admissao = st.text_input(
                            "Data Admissão",
                            value=str(pessoa_dados.get("data_admissao") or ""),
                        )

                        projetos_existentes = [
                            p.strip()
                            for p in str(
                                pessoa_dados.get("projeto") or "MCTI"
                            ).split(",")
                            if p.strip()
                        ]
                        edit_projetos = st.multiselect(
                            "Projetos / Contratos de Atuação",
                            [
                                "MCTI",
                                "MEC",
                                "COPASA",
                                "Globalweb",
                                "Start Caoa",
                            ],
                            default=projetos_existentes,
                        )

                    btn_salvar_edicao = st.form_submit_button(
                        "💾 Salvar Alterações no Cadastro"
                    )

                    if btn_salvar_edicao:
                        cargo_final = (
                            f"{edit_cargo_sel} - {edit_cargo_comp}"
                            if edit_cargo_comp
                            else edit_cargo_sel
                        )
                        string_proj = ", ".join(edit_projetos)

                        dados_atualizados = {
                            "nome": edit_nome,
                            "cargo": cargo_final,
                            "email": edit_email,
                            "telefone": edit_telefone,
                            "data_admissao": edit_admissao,
                            "projeto": string_proj,
                        }

                        st.session_state.db.atualizar_pessoa(
                            pessoa_dados["id"], dados_atualizados
                        )
                        st.success(
                            f"✅ Cadastro de **{edit_nome}** atualizado com"
                            " sucesso!"
                        )
                        st.rerun()

                st.markdown("---")
                st.subheader("🔑 Redefinição de Senha Corporativa")
                st.caption(
                    "Funcionalidade restrita a Gestores e Devs para suporte e"
                    " reset de credenciais."
                )

                with st.form("form_alterar_senha_admin"):
                    col_s1, col_s2 = st.columns([2, 1])

                    with col_s1:
                        nova_senha_input = st.text_input(
                            "Nova Senha de Acesso",
                            type="password",
                            placeholder="Digite a nova senha...",
                        )

                    with col_s2:
                        st.write("")
                        st.write("")
                        btn_redefinir_senha = st.form_submit_button(
                            "🔒 Redefinir Senha"
                        )

                    if btn_redefinir_senha:
                        if nova_senha_input:
                            st.session_state.db.alterar_senha_pessoa(
                                pessoa_dados["id"], nova_senha_input
                            )
                            st.success(
                                f"✅ Senha do colaborador"
                                f" **{str(pessoa_dados.get('nome') or '')}** redefinida no"
                                " banco!"
                            )
                            st.balloons()
                        else:
                            st.warning(
                                "⚠️ Digite uma nova senha válida antes de"
                                " salvar."
                            )

        elif nivel_acesso == "supervisor":
            st.info(
                "🔒 **Acesso restrito para edição:** Supervisores podem"
                " visualizar a lista de colaboradores, mas alterações"
                " cadastrais são permitidas apenas para **Gestores e"
                " Administradores**."
            )

        else:
            st.warning(
                "⚠️ Operadores não possuem permissão para alterar cadastros de"
                " equipe."
            )

    else:
        st.info("Nenhum colaborador encontrado na base.")

# ------------------------------------------------------------------------------
# TELA 2: CADASTRO DE PESSOAS
# ------------------------------------------------------------------------------
elif menu == "👤 Cadastrar Pessoa":
    st.title("Cadastrar Novo Colaborador")
    st.caption(
        "Preencha as informações abaixo para adicionar a pessoa à equipe."
    )

    nivel_atual = obter_nivel_permissao()
    if nivel_atual != "admin":
        st.warning(
            "⚠️ **Acesso Restrito:** Apenas **Gestores, Administradores e"
            " Devs** podem cadastrar novos colaboradores."
        )
        st.stop()

    with st.form("form_cadastrar_pessoa_menu"):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome Completo")

            cargo_selecionado = st.selectbox(
                "Cargo / Função Corporativa",
                [
                    "Gestor de TI",
                    "Coordenador de Operações",
                    "Dev / Analista de Sistemas",
                    "Supervisor de Atendimento",
                    "Líder Técnico",
                    "Analista de Suporte",
                    "Operador de Call Center",
                    "Técnico de Campo",
                ],
            )
            cargo_complemento = st.text_input(
                "Especificação da Função (Opcional)",
                placeholder="Ex: Nível 2 / Noite",
            )
            cargo_final = (
                f"{cargo_selecionado} - {cargo_complemento}"
                if cargo_complemento
                else cargo_selecionado
            )

            email = st.text_input("E-mail Corporativo")
            telefone = st.text_input("Telefone / Celular")

        with col2:
            data_admissao = st.text_input("Data Admissão (ex: 16/08/2026)")
            projetos = st.multiselect(
                "Projetos / Contratos de Atuação",
                ["MCTI", "MEC", "COPASA", "Globalweb", "Start Caoa"],
                default=["MCTI"],
            )
            senha = st.text_input("Senha de acesso", type="password")

        btn_cadastrar = st.form_submit_button(
            "✨ Confirmar e Salvar Cadastro"
        )

        if btn_cadastrar:
            if nome and email and senha and projetos:
                string_proj = ", ".join(projetos)

                nova_pessoa_dict = {
                    "nome": nome,
                    "cargo": cargo_final,
                    "email": email,
                    "telefone": telefone,
                    "data_admissao": data_admissao,
                    "projeto": string_proj,
                    "senha": senha,
                }

                try:
                    st.session_state.db.salvar_pessoa(nova_pessoa_dict)
                    st.success(
                        f"✅ Colaborador **{nome}** (`{cargo_final}`)"
                        " cadastrado no banco com sucesso!"
                    )
                except Exception as e:
                    st.error(f"⚠️ Erro ao cadastrar colaborador: {e}")
            else:
                st.warning(
                    "⚠️ Preencha Nome, E-mail, Senha e escolha pelo menos 1"
                    " Projeto."
                )

# ------------------------------------------------------------------------------
# TELA 3: ABERTURA DE CHAMADO
# ------------------------------------------------------------------------------
elif menu == "🎫 Abertura de Chamado":
    st.title("🎫 Abertura Rápida e Inteligente de Chamado")
    st.caption(
        "Triagem reativa com IA, geração de scripts técnicos e pré-visualização"
        " antes do registro."
    )

    pessoas_banco = (
        st.session_state.db.listar_pessoas()
        if hasattr(st.session_state.db, "listar_pessoas")
        else []
    )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        proj_escolhido = st.selectbox(
            "🏢 Projeto / Contrato do Cliente",
            ["MCTI", "COPASA", "MEC", "START CAOA", "Globalweb"],
            key="sb_projeto_atendimento",
        )
    with col_p2:
        opcoes_solic = (
            [
                f"{p.get('nome')} ({p.get('cargo', 'Cliente')})"
                for p in pessoas_banco
            ]
            if pessoas_banco
            else []
        )
        opcoes_solic.append("➕ Digitar Nome Manualmente")

        solic_sel = st.selectbox(
            "👤 Solicitante (Cliente / Servidor)",
            options=opcoes_solic,
            key="sb_solic_clean",
        )

        if "➕ Digitar" in str(solic_sel):
            solicitante_final = st.text_input(
                "Nome do Solicitante",
                placeholder="Digite o nome completo...",
                key="txt_solic_manual",
            )
        else:
            solicitante_final = str(solic_sel).split(" (")[0]

    st.markdown("---")


    def processar_relato_ia():
        relato = str(st.session_state.get("input_relato_ia") or "")
        if relato.strip():
            sugestao = agent_ai.classificar_chamado(
                relato,
                gerenciador_port.contratos,
                gerenciador_port.categorias_tecnicas,
            )
            cat_sug = sugestao.get("categoria", "Outros")
            subcat_sug = sugestao.get("subcategoria", "Geral")

            st.session_state["sugestao_cat"] = cat_sug
            st.session_state["sugestao_subcat"] = subcat_sug

            relato_limpo = (
                relato.replace("internnet", "internet")
                .replace("infotma", "informa")
                .replace("solciita", "solicita")
                .replace("equipamentno", "equipamento")
                .strip()
            )
            st.session_state["txt_resumo_conf"] = (
                f"Solicitação de {subcat_sug} - {relato_limpo[:60]}"
            )

            st.session_state["ta_desc_conf"] = agent_ai.polir_descricao(
                relato,
                str(cat_sug),
                str(subcat_sug),
                str(solicitante_final),
            )


    st.text_area(
        "📝 O que o cliente/servidor relatou? (Texto Livre)",
        placeholder="Ex: Colaboradora informa que não consegue acessar a pasta de rede COPASA...",
        height=100,
        key="input_relato_ia",
        on_change=processar_relato_ia,
    )

    col_b1, col_b2 = st.columns([1, 2])
    with col_b1:
        if st.button(
                "✨ Analisar e Processar com IA",
                type="primary",
                use_container_width=True,
        ):
            if str(st.session_state.get("input_relato_ia") or "").strip():
                processar_relato_ia()
                st.success("✨ IA processou o relato e ajustou o chamado!")
                st.rerun()
            else:
                st.warning(
                    "⚠️ Digite o relato do cliente no campo acima antes de"
                    " acionar a IA."
                )
    with col_b2:
        st.caption(
            "Clique para preencher as categorias e gerar o laudo técnico"
            " instantaneamente."
        )

    st.markdown("---")

    if (
            str(st.session_state.get("input_relato_ia") or "").strip()
            and "sugestao_cat" not in st.session_state
    ):
        processar_relato_ia()

    categorias = list(gerenciador_port.categorias_tecnicas.keys())
    cat_sug_val = str(st.session_state.get("sugestao_cat") or "")

    idx_cat = 0
    if cat_sug_val:
        for i, c in enumerate(categorias):
            if (
                    cat_sug_val.lower() in c.lower()
                    or c.lower() in cat_sug_val.lower()
                    or ("acesso" in cat_sug_val.lower() and "acesso" in c.lower())
            ):
                idx_cat = i
                break

    col_cat1, col_cat2, col_cat3 = st.columns(3)

    with col_cat1:
        cat_escolhida = st.selectbox(
            "📁 Categoria (IA)", categorias, index=idx_cat, key="sb_cat_conf"
        )

    subcategorias = gerenciador_port.categorias_tecnicas.get(
        str(cat_escolhida), ["Geral"]
    )
    subcat_sug_val = str(st.session_state.get("sugestao_subcat") or "")

    idx_subcat = 0
    if subcat_sug_val:
        for i, sc in enumerate(subcategorias):
            if (
                    subcat_sug_val.lower() in sc.lower()
                    or sc.lower() in subcat_sug_val.lower()
            ):
                idx_subcat = i
                break

    with col_cat2:
        subcat_escolhida = st.selectbox(
            "📂 Subcategoria (IA)",
            subcategorias,
            index=idx_subcat,
            key="sb_subcat_conf",
        )

    with col_cat3:
        impacto_escolhido = st.select_slider(
            "⚠️ Impacto",
            options=["Baixo", "Médio", "Alto"],
            value="Baixo",
            key="slider_impacto_conf",
        )
        regras_sla = {"Alto": "02 horas", "Médio": "08 horas", "Baixo": "24 horas"}
        prazo_sla = regras_sla.get(str(impacto_escolhido), "24 horas")

    st.markdown("---")

    if "txt_resumo_conf" not in st.session_state:
        st.session_state["txt_resumo_conf"] = ""
    if "ta_desc_conf" not in st.session_state:
        st.session_state["ta_desc_conf"] = ""

    resumo_final = st.text_input(
        "📌 Resumo Curto da Demanda",
        placeholder="Resumo gerado automaticamente pela IA...",
        key="txt_resumo_conf",
    )

    descricao_final = st.text_area(
        "📄 Descrição Técnica Final (Gerada pela IA / Editável)",
        height=220,
        key="ta_desc_conf",
    )

    with st.expander(
            "🛠️ Informações Complementares (Aprovador, Patrimônio, IP e Sala)"
    ):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            superior_imediato = st.text_input(
                "👔 Superior Imediato / Aprovador",
                placeholder="Ex: Dr. Carlos Mendes - Chefe de TI",
                key="txt_aprovador",
            )
            patrimonio = st.text_input(
                "💻 Nº Patrimônio / EST",
                placeholder="Ex: EST-9948",
                key="txt_patrimonio",
            )
        with col_c2:
            andar_sala = st.text_input(
                "📍 Andar / Sala",
                placeholder="Ex: 4º Andar - Sala 402",
                key="txt_sala",
            )
            endereco_ip = st.text_input(
                "🌐 Endereço IP", placeholder="Ex: 192.168.1.50", key="txt_ip"
            )

    st.markdown("---")

    st.subheader("👁️ Pré-visualização do Ticket de Atendimento")

    proximo_id = (
        st.session_state.db.obter_proximo_id()
        if hasattr(st.session_state.db, "obter_proximo_id")
        else 1
    )
    protocolo_previsto = f"{proj_escolhido}-2026-{proximo_id:04d}"

    with st.container(border=True):
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            st.markdown(f"**Protocolo:** `{protocolo_previsto}`")
            st.markdown(
                f"**Solicitante:** {solicitante_final if solicitante_final else 'N/A'}"
            )
            st.markdown(f"**Projeto:** `{proj_escolhido}`")

        with col_v2:
            st.markdown(f"**Categoria:** {cat_escolhida}")
            st.markdown(f"**Subcategoria:** {subcat_escolhida}")
            st.markdown(f"**SLA Previsto:** `{prazo_sla}`")

        with col_v3:
            st.markdown(
                f"**Aprovador:** {superior_imediato if superior_imediato else 'N/A'}"
            )
            st.markdown(
                f"**Patrimônio/EST:** {patrimonio if patrimonio else 'N/A'}"
            )
            operador_nome = "Operador"
            if (
                    st.session_state.usuario_logado
                    and isinstance(st.session_state.usuario_logado, dict)
            ):
                operador_nome = str(st.session_state.usuario_logado.get("nome") or "Operador")

            st.markdown(f"**Operador:** `{operador_nome}`")

        st.markdown("---")
        st.markdown(
            f"**Resumo:** {resumo_final if resumo_final else '*Aguardando resumo da IA...*'}"
        )
        st.caption("Laudo Técnico Gerado:")
        st.code(
            descricao_final
            if descricao_final
            else "Aguardando relato do cliente para a IA gerar o laudo...",
            language="markdown",
        )

    st.write("")

    if st.button(
            "🚀 Confirmar e Registrar Chamado",
            type="primary",
            use_container_width=True,
    ):
        if (
                solicitante_final
                and str(resumo_final).strip()
                and str(descricao_final).strip()
        ):
            operador_reg = "Operador"
            if (
                    st.session_state.usuario_logado
                    and isinstance(st.session_state.usuario_logado, dict)
            ):
                operador_reg = str(st.session_state.usuario_logado.get("nome") or "Operador")

            novo_chamado = {
                "protocolo": protocolo_previsto,
                "solicitante": solicitante_final,
                "superior_imediato": superior_imediato,
                "projeto": proj_escolhido,
                "categoria": cat_escolhida,
                "subcategoria": subcat_escolhida,
                "resumo": resumo_final,
                "patrimonio": patrimonio,
                "andar_sala": andar_sala,
                "ip": endereco_ip,
                "descricao": descricao_final,
                "impacto": impacto_escolhido,
                "prazo_sla": prazo_sla,
                "operador": operador_reg,
                "status": "Aberto",
            }

            # 1. Salva o chamado no banco de dados
            st.session_state.db.salvar_chamado(novo_chamado)
            st.toast("✅ Chamado validado e enviado com sucesso!", icon="🎉")
            st.session_state.menu_selecionado = "📊 Histórico de Chamados"  # Ajuste para o nome exato da sua aba de histórico no menu
            st.rerun()
        else:
            st.error(
                "⚠️ Preencha o Solicitante, o Resumo e a Descrição antes de"
                " registrar o chamado."
            )

# ------------------------------------------------------------------------------
# TELA 4: RELATÓRIOS INTELIGENTES COM AGENTE IA
# ------------------------------------------------------------------------------
elif menu == "📊 Relatórios Inteligentes":
    st.title("🤖 Relatórios Inteligentes & Assistente de Gestão")
    st.caption("Digite o que deseja analisar ou selecione um histórico.")

    # Inicializa histórico no session_state
    if "historico_prompts" not in st.session_state:
        st.session_state.historico_prompts = []

    # Garante que o input_prompt_relatorio exista no session_state
    if "input_prompt_relatorio" not in st.session_state:
        st.session_state.input_prompt_relatorio = ""

    # Área de histórico
    if st.session_state.historico_prompts:
        st.caption("🕒 **Histórico de buscas recentes:**")
        cols_hist = st.columns(len(st.session_state.historico_prompts))
        for i, hist in enumerate(st.session_state.historico_prompts):
            if cols_hist[i].button(f"♻️ {hist}", key=f"btn_hist_{i}"):
                st.session_state.input_prompt_relatorio = hist
                st.rerun()

    with st.form("form_relatorio_ia"):
        prompt_gestor = st.text_input(
            "🔎 O que você deseja ver no relatório?",
            placeholder="Ex: Quero ver todos os chamados críticos do MCTI...",
            key="input_prompt_relatorio"
        )
        btn_executar_ia = st.form_submit_button("🔍 Executar Análise Inteligente", type="primary",
                                                use_container_width=True)

    # Lógica do Histórico (salva apenas se houver busca)
    if btn_executar_ia and str(prompt_gestor or "").strip():
        if prompt_gestor not in st.session_state.historico_prompts:
            st.session_state.historico_prompts.insert(0, prompt_gestor)
            st.session_state.historico_prompts = st.session_state.historico_prompts[:5]

    chamados_todos: List[Dict[str, Any]] = st.session_state.db.listar_chamados()

    if chamados_todos:
        # Se clicar no botão ou se já houver um texto (para manter o resultado ao navegar)
        if btn_executar_ia or st.session_state.input_prompt_relatorio:
            query = str(prompt_gestor or "")
            dados_filtrados = GerenciadorRelatorios.filtrar_dados_por_ia(query, chamados_todos)

            st.markdown("---")

            if not dados_filtrados:
                st.error(
                    f"⚠️ Nenhum chamado encontrado para: **'{query}'**. Tente ajustar os termos ou selecionar outro projeto.")
            else:
                # Painel de Insights
                insights = GerenciadorRelatorios.obter_insights_executivos(dados_filtrados)
                with st.container(border=True):
                    col_in1, col_in2, col_in3, col_in4 = st.columns(4)
                    col_in1.metric("📊 Total Filtrado", insights["total"])
                    col_in2.metric("⚠️ Críticos/Altos", insights["criticos"])
                    col_in3.metric("📌 Status Predominante", insights["status_predominante"])
                    col_in4.metric("📁 Projeto Predominante", insights["projeto_frequente"])

                df_relatorio = pd.DataFrame(dados_filtrados)

                # Gráfico
                if "status" in df_relatorio.columns:
                    st.bar_chart(df_relatorio["status"].value_counts())

                # Tabela
                st.dataframe(df_relatorio, use_container_width=True, hide_index=True)

                # Exportação
                st.markdown("### 📥 Exportar")
                excel_bytes = GerenciadorRelatorios.converter_para_excel(dados_filtrados)
                st.download_button("📊 Baixar Excel (.xlsx)", excel_bytes, "relatorio.xlsx", use_container_width=True)

# ------------------------------------------------------------------------------
# TELA 5: PROJETOS / PORTFÓLIOS
# ------------------------------------------------------------------------------
elif menu == "📁 Projetos / Portfólios":
    st.title("📂 Matriz de Portfólios & Contratos")
    st.caption(
        "Guia de Referência rápida do escopo de atendimento para colaboradores e"
        " gestores."
    )

    col_m1, col_m2, col_m3 = st.columns(3)
    total_contratos = len(gerenciador_port.contratos)
    total_cats = len(gerenciador_port.categorias_tecnicas)
    total_subcats = sum(
        len(subs) for subs in gerenciador_port.categorias_tecnicas.values()
    )

    col_m1.metric("🏢 Contratos Ativos", total_contratos)
    col_m2.metric("📁 Categorias Principais", total_cats)
    col_m3.metric("📄 Subcategorias Mapeadas", total_subcats)

    st.markdown("---")

    tab_contratos, tab_esqueleto = st.tabs(
        ["🏢 Contratos & Clientes", "🌳 Esqueleto do Catálogo Técnico"]
    )

    with tab_contratos:
        st.subheader("Lista de Contratos Habilitados")
        st.info("Projetos e empresas atualmente atendidos pela operação.")
        for contrato in gerenciador_port.contratos:
            st.markdown(f"- **{contrato}**")

    with tab_esqueleto:
        st.subheader("Árvore de Categorias e Subcategorias")
        st.write(
            "Expanda as categorias para consultar o escopo detalhado de cada"
            " área de suporte:"
        )

        for cat, subcats in gerenciador_port.categorias_tecnicas.items():
            with st.expander(f"📁 {cat} | ({len(subcats)} Subcategorias)"):
                for subcat in subcats:
                    st.write(f"- {subcat}")

# ------------------------------------------------------------------------------
# TELA 6: PAINEL DE HISTÓRICO DE CHAMADOS & FILTROS AVANÇADOS
# ------------------------------------------------------------------------------
elif menu == "📊 Histórico de Chamados":

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0f172a !important;
            color: #f8fafc;
        }
        div[data-testid="stMetricValue"] {
            color: #38bdf8 !important;
        }
        div[data-testid="stForm"] {
            background-color: #1e293b !important;
            border-radius: 10px;
            border: 1px solid #334155 !important;
        }
        .filter-card {
            background-color: #1e293b;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #334155;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("📊 Painel de Controle e Histórico de Chamados")
    st.caption(
        "Filtros por período, buscas avançadas, gerenciamento de status e"
        " impressão de OS."
    )

    chamados_todos: List[Dict[str, Any]] = st.session_state.db.listar_chamados()
    usr_atual: Any = st.session_state.get("usuario_logado") or {}
    nome_usuario_logado: str = (
        str(usr_atual.get("nome") or "Operador")
        if isinstance(usr_atual, dict)
        else "Operador"
    )
    nivel_acesso: str = str(obter_nivel_permissao())

    # Botão no topo da aba para voltar a abrir um novo chamado rapidamente
    if st.button("➕ Abrir Novo Chamado", type="primary", use_container_width=True):
        st.session_state.menu_selecionado = "🎫 Abertura de Chamado"  # Substitua pelo nome exato da sua aba de cadastro no menu
        st.rerun()

    if chamados_todos:
        with st.form("form_filtros_chamados"):
            st.markdown("### 🔍 Filtros de Pesquisa")
            col_f1, col_f2, col_f3 = st.columns([2, 2, 1.5])

            with col_f1:
                hoje = date.today()
                data_inicio = date(hoje.year, 1, 1)
                periodo_raw = st.date_input(
                    "📅 Período de Abertura (Início e Fim):",
                    value=(data_inicio, hoje),
                    key="filtro_datas",
                )

            with col_f2:
                termo_busca: str = str(
                    st.text_input(
                        "🔎 Buscar por Solicitante, E-mail, Projeto ou Operador:",
                        placeholder="Digite o nome, projeto ou operador...",
                        key="txt_busca_geral",
                    )
                    or ""
                )

            with col_f3:
                status_filtro: str = str(
                    st.selectbox(
                        "📌 Filtrar por Status:",
                        options=[
                            "Todos",
                            "Aberto",
                            "Em Andamento",
                            "Suspenso",
                            "Aguardando Autorização",
                            "Fechado / Concluído",
                        ],
                        key="sb_status_filtro",
                    )
                    or "Todos"
                )

            btn_buscar = st.form_submit_button(
                "🔍 Buscar / Aplicar Filtros", type="primary", use_container_width=True
            )

        d_inicio: Optional[date] = None
        d_fim: Optional[date] = None

        if isinstance(periodo_raw, (tuple, list)):
            if len(periodo_raw) > 0 and isinstance(periodo_raw[0], date):
                d_inicio = periodo_raw[0]
            if len(periodo_raw) > 1 and isinstance(periodo_raw[1], date):
                d_fim = periodo_raw[1]
            elif d_inicio is not None:
                d_fim = d_inicio
        elif isinstance(periodo_raw, date):
            d_inicio = periodo_raw
            d_fim = periodo_raw

        chamados_filtrados: List[Dict[str, Any]] = []

        for c in chamados_todos:
            data_valida = True
            raw_data = str(c.get("data_abertura") or "").split(" ")[0]
            if raw_data and d_inicio is not None and d_fim is not None:
                try:
                    dt_obj = datetime.strptime(raw_data, "%d/%m/%Y").date()
                    if not (d_inicio <= dt_obj <= d_fim):
                        data_valida = False
                except ValueError:
                    pass

            texto_valido = True
            termo_limpo = termo_busca.strip().lower()
            if termo_limpo:
                campos = [
                    str(c.get("solicitante") or "").lower(),
                    str(c.get("email") or "").lower(),
                    str(c.get("projeto") or "").lower(),
                    str(c.get("operador") or "").lower(),
                    str(c.get("protocolo") or "").lower(),
                ]
                if not any(termo_limpo in campo for campo in campos):
                    texto_valido = False

            status_valido = True
            if status_filtro != "Todos":
                status_chamado = str(c.get("status") or "Aberto")
                if status_chamado.lower() != status_filtro.lower():
                    status_valido = False

            if data_valida and texto_valido and status_valido:
                chamados_filtrados.append(c)

        st.markdown("---")

        tab_listagem, tab_gestao, tab_impressao = st.tabs(
            [
                "📋 Tabela de Resultados",
                "💬 Histórico, Comentários e Status",
                "🖨️ Visualizar e Imprimir OS",
            ]
        )

        with tab_listagem:
            c1, c2, c3 = st.columns(3)
            c1.metric("Resultados Encontrados", len(chamados_filtrados))
            c2.metric("Total no Banco", len(chamados_todos))
            c3.metric("Filtro Ativo", status_filtro)

            # 1. Cria uma lista de opções baseada nos protocolos/IDs disponíveis para seleção rápida

            # Seleção rápida e segura por selectbox (compatível com qualquer Streamlit)
            with tab_listagem:
                # 1. Cria o dicionário com os chamados filtrados antes de exibir o selectbox
                opcoes_chamados = {}
                if chamados_filtrados:
                    opcoes_chamados = {
                        f"#{c.get('id')} - {c.get('protocolo')} ({c.get('solicitante')})": c
                        for c in chamados_filtrados
                    }

                # 2. Agora o restante do seu código continua daqui para baixo:
                if opcoes_chamados:
                    col_s1, col_s2 = st.columns([3, 1])
                    with col_s1:
                        escolha_label = st.selectbox(
                            label="🔍 Selecione um chamado para ver os detalhes:",
                            options=list(opcoes_chamados.keys()),
                            key="selectbox_detalhe_chamado"
                        )
                    with col_s2:
                        st.write("")
                        st.write("")
                        if st.button(label="📂 Abrir Detalhes", type="primary", use_container_width=True):
                            chamado_escolhido = opcoes_chamados[escolha_label]
                            modal_detalhes_chamado(chamado_escolhido)
                else:
                    st.info("Nenhum chamado disponível para seleção.")

                st.markdown("---")

                # Exibe a sua tabela normalmente logo abaixo
                st.dataframe(
                    chamados_filtrados,
                    use_container_width=True,
                    column_config={
                        # ... (mantenha suas configurações de colunas atuais) ...
                    },
                    hide_index=True,
                )


            # 2. Captura o clique na linha da tabela e abre a janela pop-up automaticamente
            #linhas_selecionadas = evento_tabela.selection.rows


            #if linhas_selecionadas:
            #    indice = linhas_selecionadas[0]
            #    chamado_clicado = chamados_filtrados[indice]

                # Chama o modal flutuante que criamos no topo do código
            #    modal_detalhes_chamado(chamado_clicado)

            st.markdown("---")
            with st.expander("👁️ **Pré-visualizar Descrição e Laudo Completo do Chamado**", expanded=False):
                if chamados_filtrados:
                    opcoes_prev: Dict[str, Dict[str, Any]] = {}
                    for c in chamados_filtrados:
                        proto_raw: Any = c.get("protocolo") or f"ID #{c.get('id')}"
                        solic_raw: Any = c.get("solicitante") or ""
                        resum_raw: Any = c.get("resumo") or ""

                        p_proto: str = str(proto_raw)
                        p_solic: str = str(solic_raw)
                        p_resum: str = str(resum_raw)

                        chave_v: str = f"{p_proto} | {p_solic} - {p_resum}"
                        opcoes_prev[chave_v] = c

                    chamado_prev_sel: str = str(
                        st.selectbox(
                            "Selecione um chamado da lista filtrada para visualizar os detalhes:",
                            options=list(opcoes_prev.keys()),
                            key="sb_preview_chamado_tab1",
                        )
                        or ""
                    )

                    if chamado_prev_sel in opcoes_prev:
                        ticket_p: Dict[str, Any] = opcoes_prev[chamado_prev_sel]

                        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
                        col_p1.markdown(f"**Protocolo:** `{str(ticket_p.get('protocolo') or '')}`")
                        col_p2.markdown(f"**Solicitante:** {str(ticket_p.get('solicitante') or '')}")
                        col_p3.markdown(f"**Contrato:** `{str(ticket_p.get('projeto') or '')}`")
                        col_p4.markdown(f"**Status:** `{str(ticket_p.get('status') or 'Aberto')}`")

                        st.markdown("##### 📄 Relato do Cliente / Laudo Técnico:")
                        desc_p: str = str(ticket_p.get("descricao") or "Sem descrição cadastrada.")

                        partes_p: List[str] = desc_p.split("\n\n--- ")
                        laudo_p: str = partes_p[0]
                        interacoes_p: List[str] = partes_p[1:] if len(partes_p) > 1 else []

                        with st.container(border=True):
                            st.markdown(laudo_p)

                        if interacoes_p:
                            st.markdown("##### 💬 Histórico de Interações:")
                            for item in interacoes_p:
                                linhas_i: List[str] = item.split("\n", 1)
                                cab_i: str = linhas_i[0].replace("---", "").strip()
                                corp_i: str = linhas_i[1] if len(linhas_i) > 1 else ""

                                with st.container(border=True):
                                    st.markdown(f"**{cab_i}**")
                                    st.caption(corp_i)
                else:
                    st.info("Nenhum chamado encontrado para pré-visualização.")

        with tab_gestao:

            if chamados_filtrados:
                opcoes_chamados_gestao: Dict[str, Dict[str, Any]] = {}
                for c in chamados_filtrados:
                    proto_raw: Any = c.get("protocolo") or f"ID #{c.get('id')}"
                    status_raw: Any = c.get("status") or "Aberto"
                    solic_raw: Any = c.get("solicitante") or ""
                    proj_raw: Any = c.get("projeto") or ""

                    p_proto: str = str(proto_raw)
                    p_status: str = str(status_raw)
                    p_solic: str = str(solic_raw)
                    p_proj: str = str(proj_raw)

                    chave_gestao: str = f"{p_proto} | Status: [{p_status}] - {p_solic} ({p_proj})"
                    opcoes_chamados_gestao[chave_gestao] = c

                chamado_sel_chave = str(
                    st.selectbox(
                        "Selecione o chamado para interagir:",
                        options=list(opcoes_chamados_gestao.keys()),
                    )
                    or ""
                )

                if chamado_sel_chave in opcoes_chamados_gestao:
                    ticket_sel = opcoes_chamados_gestao[chamado_sel_chave]
                    operador_ticket = str(ticket_sel.get("operador") or "")
                    status_atual = str(
                        ticket_sel.get("status") or "Aberto"
                    )

                    pode_editar = nivel_acesso in [
                        "admin",
                        "supervisor",
                    ] or (
                                          nivel_acesso == "operador"
                                          and operador_ticket.strip().lower()
                                          == nome_usuario_logado.strip().lower()
                                  )

                    st.markdown("---")
                    c_inf1, c_inf2, c_inf3, c_inf4 = st.columns(4)
                    c_inf1.markdown(f"**Protocolo:** `{str(ticket_sel.get('protocolo') or '')}`")
                    c_inf2.markdown(f"**Solicitante:** {str(ticket_sel.get('solicitante') or '')}")
                    c_inf3.markdown(f"**Operador:** `{operador_ticket}`")
                    c_inf4.markdown(f"**Status Atual:** `{status_atual}`")

                    st.markdown("---")
                    st.markdown("### 📜 Histórico e Linha do Tempo do Atendimento")

                    descricao_full = str(ticket_sel.get("descricao") or "")
                    partes = descricao_full.split("\n\n--- ")
                    laudo_inicial = partes[0]
                    interacoes = partes[1:] if len(partes) > 1 else []

                    with st.container(border=True):
                        st.markdown("**📄 Laudo Técnico / Relato Inicial:**")
                        st.markdown(laudo_inicial)

                    if interacoes:
                        st.markdown("#### 💬 Interações e Pareceres")
                        for item in interacoes:
                            linhas = item.split("\n", 1)
                            cabecalho = linhas[0].replace("---", "").strip()
                            corpo = linhas[1] if len(linhas) > 1 else ""

                            with st.container(border=True):
                                st.markdown(f"**{cabecalho}**")
                                st.caption(corpo)

                    if pode_editar:
                        st.success(
                            "✅ **Permissão concedida:** Você é o responsável por este chamado ou possui perfil de gestão."
                        )

                        col_acao1, col_acao2 = st.columns(2)

                        with col_acao1:
                            with st.form("form_novo_comentario"):
                                st.markdown("#### 💬 Adicionar Novo Comentário")
                                novo_comentario: str = str(
                                    st.text_area(
                                        "Escreva a nota técnica ou atualização:",
                                        placeholder="Digite o andamento da solicitação...",
                                        height=100,
                                    )
                                    or ""
                                )
                                btn_comentar = st.form_submit_button(
                                    "💬 Salvar Comentário", type="primary"
                                )

                                if btn_comentar:
                                    if novo_comentario.strip():
                                        st.session_state.db.adicionar_comentario_chamado(
                                            ticket_sel["id"],
                                            nome_usuario_logado,
                                            novo_comentario,
                                        )
                                        st.success("✅ Comentário adicionado com sucesso!")
                                        st.rerun()
                                    else:
                                        st.warning("⚠️ Digite uma mensagem antes de salvar.")

                        with col_acao2:
                            with st.form("form_alterar_status"):
                                st.markdown("#### 🔄 Mudar Status do Chamado")
                                lista_status = [
                                    "Aberto",
                                    "Em Andamento",
                                    "Suspenso",
                                    "Aguardando Autorização",
                                    "Fechado / Concluído",
                                ]
                                idx_status = (
                                    lista_status.index(status_atual)
                                    if status_atual in lista_status
                                    else 0
                                )

                                novo_status: str = str(
                                    st.selectbox(
                                        "Selecione o novo status:",
                                        options=lista_status,
                                        index=idx_status,
                                    )
                                    or status_atual
                                )
                                parecer_tecnico: str = ""

                                if novo_status == "Fechado / Concluído":
                                    parecer_tecnico = str(
                                        st.text_area(
                                            "Parecer Técnico de Solução:",
                                            placeholder="Procedimentos finais tomados...",
                                            height=80,
                                        )
                                        or ""
                                    )

                                btn_atualizar_status = st.form_submit_button("💾 Salvar Novo Status")

                                if btn_atualizar_status:
                                    if (
                                            novo_status == "Fechado / Concluído"
                                            and not parecer_tecnico.strip()
                                    ):
                                        st.warning("⚠️ Preencha o parecer técnico antes de fechar.")
                                    else:
                                        st.session_state.db.atualizar_status_chamado(
                                            ticket_sel["id"],
                                            novo_status,
                                            parecer_tecnico,
                                        )
                                        st.success("🎉 Chamado finalizado com êxito!")
                                        col_f1, col_f2 = st.columns(2)
                                        col_f1.metric("📁 Status", f"{novo_status}")
                                        col_f2.metric("⏱️ SLA", "Dentro do Prazo")
                    else:
                        st.error(
                            f"🔒 **Acesso Restrito:** Chamado atribuído a **{operador_ticket}**. Operadores podem interagir apenas em seus próprios chamados."
                        )
            else:
                st.info("Nenhum chamado corresponde aos filtros aplicados.")

        with tab_impressao:
            if chamados_filtrados:
                opcoes_impressao: List[str] = []
                for c in chamados_filtrados:
                    p_proto: str = str(c.get("protocolo") or f"ID #{c.get('id')}")
                    p_proj: str = str(c.get("projeto") or "")
                    p_resum: str = str(c.get("resumo") or "")

                    opcoes_impressao.append(f"{p_proto} - {p_proj} ({p_resum})")

                chamado_sel_imp = str(
                    st.selectbox("Selecione para gerar a OS:", opcoes_impressao)
                    or ""
                )

                if chamado_sel_imp in opcoes_impressao:
                    idx_imp = opcoes_impressao.index(chamado_sel_imp)
                    ticket_imp = chamados_filtrados[idx_imp]

                    with st.container(border=True):
                        col_l, col_t = st.columns([1, 4])
                        with col_l:
                            st.image("logo.png", width=90)
                        with col_t:
                            st.markdown(
                                "## 🎫 Ordem de Serviço -"
                                f" {str(ticket_imp.get('protocolo') or '')}"
                            )
                            st.caption(
                                f"Abertura: {str(ticket_imp.get('data_abertura') or '')} |"
                                f" Status: {str(ticket_imp.get('status') or '')}"
                            )

                        st.markdown("---")
                        c_i1, c_i2, c_i3, c_i4 = st.columns(4)
                        c_i1.markdown(f"**Solicitante:**\n{str(ticket_imp.get('solicitante') or '')}")
                        c_i2.markdown(f"**Projeto:**\n{str(ticket_imp.get('projeto') or '')}")
                        c_i3.markdown(f"**Categoria:**\n{str(ticket_imp.get('categoria') or '')}")
                        c_i4.markdown(f"**Impacto:**\n{str(ticket_imp.get('impacto') or '')}")

                        st.markdown("---")
                        st.markdown("### 📝 Descrição e Histórico")
                        st.info(f"**Resumo:** {str(ticket_imp.get('resumo') or '')}")
                        st.markdown(str(ticket_imp.get("descricao") or ""))
    else:
        st.info("📭 Nenhum chamado encontrado na base de dados.")

