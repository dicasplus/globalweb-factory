import streamlit as st

from app.ai_agent import AgenteAtendimento
from app.database import DatabaseManager
from app.pessoas import GerenciadorPessoas, Pessoa
from app.portfolios import GerenciadorPortfolios

# ==============================================================================
# FUNÇÃO DE CONTROLE DE PERMISSÕES (RBAC)
# ==============================================================================
def obter_nivel_permissao():
    """Retorna o nível de acesso do usuário logado: 'admin', 'supervisor' ou 'operador'."""
    usuario = st.session_state.get("usuario_logado")
    if not usuario:
        return "visitante"

    cargo = usuario.get("cargo", "").lower()

    # Define as palavras-chave para cada perfil
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
# 🔹 CONFIGURAÇÕES INICIAIS DA APLICAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="GLOBAL WEB FACTORY", page_icon=":robot_face:", layout="wide"
)

# 1.2. Inicialização da Memória da Sessão (Garante as variáveis no session_state)
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "menu_selecionado" not in st.session_state:
    st.session_state.menu_selecionado = "🏠 Início"
# ==============================================================================
# 2. REDIRECIONAMENTO AUTOMÁTICO POR PERFIL DE ACESSO
# ==============================================================================
if st.session_state.get("usuario_logado") is not None:
    nivel_atual = obter_nivel_permissao()

    # Se for operador, força a abertura na tela de Chamados na primeira carga
    if nivel_atual == "operador" and "redirecionado" not in st.session_state:
        st.session_state.menu_selecionado = "🎫 Abertura de Chamado"
        st.session_state.redirecionado = True

# ==============================================================================
# 🔹 INICIALIZAÇÃO DA MEMÓRIA DA SESSÃO (SESSION STATE)
# ==============================================================================
if "db" not in st.session_state:
    st.session_state.db = DatabaseManager()

if "gerenciador" not in st.session_state:
    st.session_state["gerenciador"] = GerenciadorPessoas()
    # Pessoas iniciais para teste
    p1 = Pessoa(
        "Charles Ferreira de Moura",
        "Dev Junior",
        "charles@empresa.com",
        "61 9999-9999",
        "01/08/2024",
        "MCTI, COPASA",  # Exemplo com múltiplos projetos
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

gerenciador_port = st.session_state.gerenciador_portfolios
agent_ai = st.session_state.agent_ai


# ==============================================================================
# MENU DE NAVEGAÇÃO LATERAL (Condicional de Autenticação)
# ==============================================================================
# 1. Garante que as variáveis do controle de sessão existam
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "menu_selecionado" not in st.session_state:
    st.session_state.menu_selecionado = "🏠 Início"

# 2. Se NÃO estiver logado, esconde a barra lateral e fixa a tela em Início
if st.session_state.usuario_logado is None:
    menu = "🏠 Início"
else:
    # 🟢 USUÁRIO LOGADO: Desenha a barra lateral completa
    with st.sidebar:
        st.image("logo.png", use_container_width=True)

        usuario = st.session_state.usuario_logado
        st.markdown(f"### 👤 {usuario['nome']}")
        st.caption(f"Cargo: {usuario['cargo']}")
        st.markdown("---")

        opcoes_menu = [
            "🏠 Início",
            "📋 Listar Pessoas",
            "👤 Cadastrar Pessoa",
            "🎫 Abertura de Chamado",
            "📊 Histórico de Chamados",
            "📁 Projetos / Portfólios",
        ]

        menu = st.radio(
            "Navegação",
            opcoes_menu,
            index=opcoes_menu.index(st.session_state.menu_selecionado),
        )
        st.session_state.menu_selecionado = menu

        st.markdown("---")

        # Botão rápido de Logout na própria barra lateral
        if st.button("🚪 Sair da Conta", type="secondary"):
            st.session_state.usuario_logado = None
            st.session_state.menu_selecionado = "🏠 Início"
            st.rerun()
# ------------------------------------------------------------------------------
# TELA 0: INÍCIO
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# TELA 0: INÍCIO (Com Login, Boas-Vindas e Cadastro rápido)
# ------------------------------------------------------------------------------
if menu == "🏠 Início":

    # 1. Garante que o estado 'usuario_logado' exista na sessão do Streamlit
    if "usuario_logado" not in st.session_state:
        st.session_state.usuario_logado = None

    # --------------------------------------------------------------------------
    # 🌟 CENÁRIO A: USUÁRIO JÁ ESTÁ LOGADO
    # --------------------------------------------------------------------------
    if st.session_state.usuario_logado is not None:
        usuario = st.session_state.usuario_logado

        # Cabeçalho personalizado com o nome do colaborador
        st.success(f"👋 Bem-vindo(a) de volta, **{usuario['nome']}**!")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("logo.png", use_container_width=True)

        st.markdown(
            "<h1 style='text-align: center;'>GlobalWeb Factory</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h3 style='text-align: center; color:#888;'>Painel de Operações - {usuario['cargo']}</h3>",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ----------------------------------------------------------------------
        # 📊 1. BUSCA E FILTRO UNIFICADO DE CONTRATOS (HUB OMNICHANNEL)
        # ----------------------------------------------------------------------
        chamados_todos = st.session_state.db.listar_chamados()

        # Lista de projetos para o filtro unificado
        projetos_disponiveis = [
            "Todos os Contratos",
            "MCTI",
            "COPASA",
            "START CAOA",
            "MEC",
            "Globalweb",
        ]

        # Filtro no topo da visão do supervisor
        col_filtro1, col_filtro2 = st.columns([2, 1])
        with col_filtro1:
            st.subheader("🏢 Visão Geral dos Contratos Integrados")
        with col_filtro2:
            contrato_selecionado = st.selectbox(
                "Filtrar por Cliente/Contrato:", projetos_disponiveis
            )

        # Aplica o filtro na lista de chamados
        if contrato_selecionado != "Todos os Contratos":
            chamados_banco = [
                c
                for c in chamados_todos
                if c.get("projeto") == contrato_selecionado
            ]
        else:
            chamados_banco = chamados_todos

        # Calculando indicadores reais para os Cards
        total_chamados = len(chamados_banco)
        chamados_urgentes = sum(
            1
            for c in chamados_banco
            if c.get("impacto") in ["Crítico / Alta", "Alto"]
        )

        # ----------------------------------------------------------------------
        # 📈 2. CARDS DE INDICADORES (KPIs REAIS)
        # ----------------------------------------------------------------------
        kpi1, kpi2, kpi3 = st.columns(3)

        with kpi1:
            st.metric(
                label="Total de Chamados",
                value=total_chamados,
                delta=contrato_selecionado,
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

        # ----------------------------------------------------------------------
        # 👤 3. SEUS DADOS DE ACESSO E AÇÕES RÁPIDAS
        # ----------------------------------------------------------------------
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"""
                    ### 👤 Seus Dados de Acesso
                    * **E-mail:** {usuario['email']}
                    * **Projetos Atribuídos:** `{usuario['projeto']}`
                    """)

        with c2:
            st.success("""
                    ### 🎫 Atendimento Ativo
                    * Utilize o menu lateral para **Abertura de Chamados**.
                    * Acompanhe os SLAs na aba de **Histórico de Chamados**.
                    """)

        st.markdown("---")

        # Botão para Encerrar a Sessão (Logout)
        if st.button("🚪 Sair do Sistema", type="secondary"):
            st.session_state.usuario_logado = None
            st.rerun()  # Recarrega a tela imediatamente para atualizar o estado

    # --------------------------------------------------------------------------
    # 🔑 CENÁRIO B: USUÁRIO AINDA NÃO FEZ LOGIN (Tela de Boas-Vindas)
    # --------------------------------------------------------------------------
    else:
        # Apresentação do Cabeçalho
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("logo.png", use_container_width=True)

        st.markdown(
            "<h1 style='text-align: center;'>GlobalWeb Factory</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color:#888;'>Portal Único de Gestão e Suporte Integrado</h3>",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # 🗂️ Abas para alternar entre Login e Novo Cadastro
        tab_login, tab_cadastro = st.tabs(
            ["🔑 Acessar Minha Conta", "📝 Não tenho cadastro (Cadastrar-me)"]
        )

        # ----------------------------------------------------------------------
        # ABA 1: FORMULÁRIO DE LOGIN
        # ----------------------------------------------------------------------
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
                    # 🟢 Busca e valida o usuário direto do banco de dados SQLite
                    colaborador = st.session_state.db.buscar_pessoa_por_login(
                        login_email, login_senha
                    )

                    if colaborador:
                        st.session_state.usuario_logado = colaborador
                        st.balloons()
                        st.success(
                            f"✅ Bem-vindo(a), **{colaborador['nome']}**!"
                        )
                        st.rerun()
                    else:
                        st.error(
                            "❌ E-mail ou senha incorretos. Verifique suas credenciais ou faça o cadastro."
                        )

        # ----------------------------------------------------------------------
        # ABA 2: FORMULÁRIO DE CADASTRO RÁPIDO (Salvando direto no SQLite)
        # ----------------------------------------------------------------------
        with tab_cadastro:
            st.subheader("Criar Novo Cadastro de Colaborador")
            st.caption(
                "Preencha os dados abaixo para salvar no banco de dados e liberar o acesso."
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
                        ["MCTI", "MEC", "COPASA", "Globalweb", "Start Caoa"],
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
                            # 🟢 Salva permanentemente no banco SQLite
                            st.session_state.db.salvar_pessoa(nova_pessoa_dict)

                            # Loga automaticamente o usuário recém-cadastrado
                            st.session_state.usuario_logado = nova_pessoa_dict

                            st.balloons()
                            st.success(
                                f"🎉 Cadastro de **{novo_nome}** salvo no banco com sucesso!"
                            )
                            st.rerun()

                        except Exception as e:
                            st.error(
                                f"⚠️ Erro ao salvar cadastro (este e-mail pode já estar cadastrado): {e}"
                            )
                    else:
                        st.warning(
                            "⚠️ Preencha Nome, E-mail, Senha e escolha pelo menos 1 Projeto."
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

    # 1. Busca colaboradores do banco de dados
    pessoas_banco = st.session_state.db.listar_pessoas()

    # Identifica o nível de acesso do usuário logado
    nivel_acesso = obter_nivel_permissao()

    if pessoas_banco:
        # Exibe a tabela principal de visualização para Supervisores e Gestores/Admin
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
                "senha": None,  # Oculta a senha
            },
            hide_index=True,
        )

        st.markdown("---")

        # ----------------------------------------------------------------------
        # ✏️ SEÇÃO DE EDIÇÃO (LIBERADA APENAS PARA ADMIN / GESTOR / DEV)
        # ----------------------------------------------------------------------
        st.subheader("✏️ Alterar Cadastro de Colaborador")


        if nivel_acesso == "admin":
            # Lista padronizada de cargos para manter a coerência do RBAC
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

            # Dicionário formatado de colaboradores
            opcoes_pessoas = {
                f"#{p['id']} - {p['nome']} ({p['cargo']})": p
                for p in pessoas_banco
            }

            pessoa_selecionada_chave = st.selectbox(
                "Selecione o colaborador que deseja editar:",
                options=list(opcoes_pessoas.keys()),
            )

            if pessoa_selecionada_chave:
                pessoa_dados = opcoes_pessoas[pessoa_selecionada_chave]

                # Identifica o cargo atual para pré-selecionar no dropdown
                cargo_atual = pessoa_dados.get("cargo", "")
                index_cargo = 0
                for idx, c in enumerate(lista_cargos_padrao):
                    if c in cargo_atual:
                        index_cargo = idx
                        break

                # --------------------------------------------------------------
                # 📝 FORMULÁRIO 1: ALTERAÇÃO DE DADOS CADASTRAIS
                # --------------------------------------------------------------
                with st.form("form_editar_pessoa"):
                    col_e1, col_e2 = st.columns(2)

                    with col_e1:
                        edit_nome = st.text_input(
                            "Nome Completo",
                            value=str(pessoa_dados.get("nome", "")),
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
                            value=str(pessoa_dados.get("email", "")),
                        )

                    with col_e2:
                        edit_telefone = st.text_input(
                            "Telefone",
                            value=str(pessoa_dados.get("telefone", "")),
                        )
                        edit_admissao = st.text_input(
                            "Data Admissão",
                            value=str(pessoa_dados.get("data_admissao", "")),
                        )

                        projetos_existentes = [
                            p.strip()
                            for p in str(
                                pessoa_dados.get("projeto", "MCTI")
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
                            f"✅ Cadastro de **{edit_nome}** atualizado com sucesso!"
                        )
                        st.rerun()

                # --------------------------------------------------------------
                # 🔑 FORMULÁRIO 2: RESET DE SENHA (INDEPENDENTE E SEPARADO)
                # --------------------------------------------------------------
                st.markdown("---")
                st.subheader("🔑 Redefinição de Senha Corporativa")
                st.caption(
                    "Funcionalidade restrita a Gestores e Devs para suporte e reset de credenciais."
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
                                f"✅ Senha do colaborador **{pessoa_dados['nome']}** redefinida no banco!"
                            )
                            st.balloons()
                        else:
                            st.warning(
                                "⚠️ Digite uma nova senha válida antes de salvar."
                            )

        elif nivel_acesso == "supervisor":
            st.info(
                "🔒 **Acesso restrito para edição:** Supervisores podem visualizar a lista de colaboradores, mas alterações cadastrais são permitidas apenas para **Gestores e Administradores**."
            )

        else:
            st.warning(
                "⚠️ Operadores não possuem permissão para alterar cadastros de equipe."
            )

    else:
        st.info("Nenhum colaborador encontrado na base.")
# ------------------------------------------------------------------------------
# TELA 2: CADASTRO DE PESSOAS (Com seleção de múltiplos projetos)
# ------------------------------------------------------------------------------
elif menu == "👤 Cadastrar Pessoa":
    st.title("Cadastrar Novo Colaborador")
    st.caption("Preencha as informações abaixo para adicionar a pessoa à equipe.")

    # 🔒 Validação de Permissão
    nivel_atual = obter_nivel_permissao()
    if nivel_atual != "admin":
        st.warning(
            "⚠️ **Acesso Restrito:** Apenas **Gestores, Administradores e Devs** podem cadastrar novos colaboradores.")
        st.stop()

    with st.form("form_cadastrar_pessoa_menu"):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome Completo")

            # Lista padronizada para garantir a regra do RBAC
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
                    "Técnico de Campo"
                ]
            )
            cargo_complemento = st.text_input("Especificação da Função (Opcional)", placeholder="Ex: Nível 2 / Noite")
            cargo_final = f"{cargo_selecionado} - {cargo_complemento}" if cargo_complemento else cargo_selecionado

            email = st.text_input("E-mail Corporativo")
            telefone = st.text_input("Telefone / Celular")

        with col2:
            data_admissao = st.text_input("Data Admissão (ex: 16/08/2026)")
            projetos = st.multiselect(
                "Projetos / Contratos de Atuação",
                ["MCTI", "MEC", "COPASA", "Globalweb", "Start Caoa"],
                default=["MCTI"]
            )
            senha = st.text_input("Senha de acesso", type="password")

        btn_cadastrar = st.form_submit_button("✨ Confirmar e Salvar Cadastro")

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
                    "senha": senha
                }

                try:
                    st.session_state.db.salvar_pessoa(nova_pessoa_dict)
                    st.success(f"✅ Colaborador **{nome}** (`{cargo_final}`) cadastrado no banco com sucesso!")
                except Exception as e:
                    st.error(f"⚠️ Erro ao cadastrar colaborador: {e}")
            else:
                st.warning("⚠️ Preencha Nome, E-mail, Senha e escolha pelo menos 1 Projeto.")

# ------------------------------------------------------------------------------
# TELA 3: ABERTURA DE CHAMADO (Reativa ao usuário e calculando SLA)
# ------------------------------------------------------------------------------
elif menu == "🎫 Abertura de Chamado":
    st.title("🎫 Abertura Rápida e Inteligente de Chamado")
    st.caption(
        "Triagem reativa com IA, geração de scripts técnicos e pré-visualização"
        " antes do registro."
    )

    # 1. IDENTIFICAÇÃO DO PROJETO E SOLICITANTE
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
                f"{p['nome']} ({p.get('cargo', 'Cliente')})"
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

        if "➕ Digitar" in solic_sel:
            solicitante_final = st.text_input(
                "Nome do Solicitante",
                placeholder="Digite o nome completo...",
                key="txt_solic_manual",
            )
        else:
            solicitante_final = solic_sel.split(" (")[0]

    st.markdown("---")

    # 2. FUNÇÃO AUXILIAR DE PROCESSAMENTO DA IA
    def processar_relato_ia():
        relato = st.session_state.get("input_relato_ia", "")
        if relato.strip():
            sugestao = agent_ai.classificar_chamado(
                relato,
                gerenciador_port.contratos,
                gerenciador_port.categorias_tecnicas,
            )
            cat = sugestao.get("categoria", "Outros")
            subcat = sugestao.get("subcategoria", "Geral")

            st.session_state["sugestao_cat"] = cat
            st.session_state["sugestao_subcat"] = subcat

            # Trata o texto para o Resumo Curto
            relato_limpo = (
                relato.replace("infotma", "informa")
                .replace("solciita", "solicita")
                .replace("nao consegue", "não consegue")
                .strip()
            )
            st.session_state["txt_resumo_conf"] = (
                f"Solicitação de {subcat} - {relato_limpo[:60]}"
            )

            # Gera a descrição técnica limpa e padronizada
            st.session_state["ta_desc_conf"] = agent_ai.polir_descricao(
                texto_bruto=relato, categoria=cat, subcategoria=subcat
            )

    # Entrada de Texto Livre
    st.text_area(
        "📝 O que o cliente/servidor relatou? (Texto Livre)",
        placeholder="Ex: Colaboradora informa que não consegue acessar a pasta de rede COPASA...",
        height=100,
        key="input_relato_ia",
        on_change=processar_relato_ia,
    )

    # ⚡ BOTÃO PRINCIPAL DA IA LOGO ABAIXO DO TEXTO LIVRE
    col_b1, col_b2 = st.columns([1, 2])
    with col_b1:
        if st.button(
            "✨ Analisar e Processar com IA",
            type="primary",
            use_container_width=True,
        ):
            if st.session_state.get("input_relato_ia", "").strip():
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
        st.session_state.get("input_relato_ia", "").strip()
        and "sugestao_cat" not in st.session_state
    ):
        processar_relato_ia()

    # 3. SELEÇÃO DE CATEGORIAS (ALINHAMENTO DA IA)
    categorias = list(gerenciador_port.categorias_tecnicas.keys())
    cat_sug = st.session_state.get("sugestao_cat")

    idx_cat = 0
    if cat_sug:
        for i, c in enumerate(categorias):
            if (
                cat_sug.lower() in c.lower()
                or c.lower() in cat_sug.lower()
                or ("acesso" in cat_sug.lower() and "acesso" in c.lower())
            ):
                idx_cat = i
                break

    col_cat1, col_cat2, col_cat3 = st.columns(3)

    with col_cat1:
        cat_escolhida = st.selectbox(
            "📁 Categoria (IA)", categorias, index=idx_cat, key="sb_cat_conf"
        )

    subcategorias = gerenciador_port.categorias_tecnicas.get(
        cat_escolhida, ["Geral"]
    )
    subcat_sug = st.session_state.get("sugestao_subcat")

    idx_subcat = 0
    if subcat_sug:
        for i, sc in enumerate(subcategorias):
            if (
                subcat_sug.lower() in sc.lower()
                or sc.lower() in subcat_sug.lower()
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
        prazo_sla = regras_sla.get(impacto_escolhido, "24 horas")

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

    # 4. CAMPOS COMPLEMENTARES ORGANIZADOS
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

    # 5. PRÉ-VISUALIZAÇÃO DO TICKET
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
            st.markdown(f"**Patrimônio/EST:** {patrimonio if patrimonio else 'N/A'}")
            st.markdown(
                f"**Operador:** `{st.session_state.usuario_logado.get('nome', 'Operador') if st.session_state.usuario_logado else 'Operador'}`"
            )

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

    # 6. REGISTRO NO BANCO SQLITE
    if st.button(
        "🚀 Confirmar e Registrar Chamado no Banco",
        type="primary",
        use_container_width=True,
    ):
        if solicitante_final and resumo_final.strip() and descricao_final.strip():
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
                "operador": (
                    st.session_state.usuario_logado.get("nome", "Operador")
                    if st.session_state.usuario_logado
                    else "Operador"
                ),
                "status": "Aberto",
            }

            st.session_state.db.salvar_chamado(novo_chamado)
            st.balloons()
            st.success(
                f"✅ Chamado **{protocolo_previsto}** criado com sucesso no"
                f" banco de dados para **{solicitante_final}**!"
            )
        else:
            st.error(
                "⚠️ Preencha o Solicitante, o Resumo e a Descrição antes de"
                " registrar o chamado."
            )

# ------------------------------------------------------------------------------
# TELA 4: PROJETOS / PORTFÓLIOS
# ------------------------------------------------------------------------------
elif menu == "📁 Projetos / Portfólios":
    st.title("📂 Matriz de Portfólios & Contratos")
    st.caption(
        "Guia de Referência rápida do escopo de atendimento para colaboradores e gestores."
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
            "Expanda as categorias para consultar o escopo detalhado de cada área de suporte:"
        )

        for cat, subcats in gerenciador_port.categorias_tecnicas.items():
            with st.expander(f"📁 {cat} | ({len(subcats)} Subcategorias)"):
                for subcat in subcats:
                    st.write(f"- {subcat}")

# ------------------------------------------------------------------------------
# TELA 5: PAINEL DE HISTÓRICO DE CHAMADOS (Com suporte aos novos campos)
# ------------------------------------------------------------------------------
elif menu == "📊 Histórico de Chamados":
    st.title("📊 Painel de Chamados Registrados")
    st.write(
        "Acompanhe o histórico de todas as solicitações salvas no banco de dados."
    )

    chamados_salvos = st.session_state.db.listar_chamados()

    if chamados_salvos:
        # Métricas do Topo
        total_chamados = len(chamados_salvos)
        chamados_altos = len(
            [c for c in chamados_salvos if c.get("impacto") == "Alto"]
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Chamados Abertos", total_chamados)
        col2.metric("Chamados de Alto Impacto", chamados_altos)
        col3.metric("Status do Banco", "Online 🟢")

        st.markdown("---")
        st.subheader("📋 Tabela de Registros")

        # Tabela formatada exibindo os novos campos de Protocolo e SLA
        st.dataframe(
            chamados_salvos,
            use_container_width=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", format="#%d"),
                "protocolo": "Protocolo",
                "data_abertura": st.column_config.DatetimeColumn(
                    "Abertura", format="DD/MM/YYYY HH:mm"
                ),
                "solicitante": "Solicitante",
                "projeto": "Contrato",
                "categoria": "Categoria",
                "subcategoria": "Subcategoria",
                "resumo": "Resumo",
                "impacto": "Impacto",
                "prazo_sla": "SLA Previsto",
                "descricao": None,
                "patrimonio": None,
                "andar_sala": None,
                "ip": None,
            },
            hide_index=True,
        )

        # ----------------------------------------------------------------------
        # 🖨️ VISUALIZAÇÃO E IMPRESSÃO DE ORDEM DE SERVIÇO
        # ----------------------------------------------------------------------
        st.markdown("---")
        st.subheader("🖨️ Visualizar e Imprimir Chamado")

        # 🟢 Forma limpa e sem erro de aspas/contra-barra:
        opcoes_chamados = ["Selecione um chamado..."] + [
            f"{c.get('protocolo') or 'ID #' + str(c['id'])} - {c['projeto']} ({c['resumo']})"
            for c in chamados_salvos
        ]

        chamado_selecionado = st.selectbox(
            "Selecione para gerar a Ordem de Serviço:", opcoes_chamados
        )

        if chamado_selecionado != "Selecione um chamado...":
            # Busca o registro pelo índice selecionado na lista
            idx_selecionado = opcoes_chamados.index(chamado_selecionado) - 1
            ticket = chamados_salvos[idx_selecionado]

            if ticket:
                # CSS para ocultar elementos do Streamlit na hora do Ctrl+P
                st.markdown(
                    """
                    <style>
                    @media print {
                        section[data-testid="stSidebar"] {display: none !important;}
                        header[data-testid="stHeader"] {display: none !important;}
                        .stSelectbox {display: none !important;}
                        button {display: none !important;}
                        .main .block-container {max-width: 100% !important; padding: 1rem !important;}
                    }
                    </style>
                """,
                    unsafe_allow_html=True,
                )

                # Ordem de Serviço Formatada
                # Ordem de Serviço Formatada
                with st.container(border=True):
                    col_logo, col_titulo = st.columns([1, 4])

                    # 🟢 Pega o protocolo ou gera a tag de ID limpa
                    protocolo_exibicao = ticket.get('protocolo') or f"ID #{ticket['id']}"

                    with col_logo:
                        st.image("logo.png", width=100)
                    with col_titulo:
                        st.markdown(f"## 🎫 Ordem de Serviço - {protocolo_exibicao}")
                        st.caption(
                            f"**Data de Abertura:** {ticket['data_abertura']} | **SLA Previsto:** {ticket.get('prazo_sla', '24 horas')}"
                        )

                    st.markdown("---")

                    c1, c2, c3, c4 = st.columns(4)
                    c1.markdown(f"**👤 Solicitante:**\n{ticket['solicitante']}")
                    c2.markdown(f"**🏢 Contrato:**\n{ticket['projeto']}")
                    c3.markdown(f"**📁 Categoria:**\n{ticket['categoria']}")
                    c4.markdown(f"**⚠️ Impacto:**\n{ticket['impacto']}")

                    if (
                        ticket["patrimonio"]
                        or ticket["andar_sala"]
                        or ticket["ip"]
                    ):
                        st.markdown("<br>", unsafe_allow_html=True)
                        c_infra1, c_infra2, c_infra3 = st.columns(3)
                        c_infra1.markdown(
                            f"**🖥️ Patrimônio:** {ticket['patrimonio'] or 'N/A'}"
                        )
                        c_infra2.markdown(
                            f"**📍 Localização:** {ticket['andar_sala'] or 'N/A'}"
                        )
                        c_infra3.markdown(
                            f"**🌐 Endereço IP:** {ticket['ip'] or 'N/A'}"
                        )

                    st.markdown("---")

                    st.markdown("### 📝 Descrição Técnica e Diagnóstico")
                    st.info(f"**Resumo:** {ticket['resumo']}")
                    st.markdown(ticket["descricao"])

                    st.markdown("<br><br>", unsafe_allow_html=True)
                    col_ass1, col_ass2 = st.columns(2)
                    col_ass1.markdown(
                        "<div style='text-align: center;'>_______________________________________<br><b>Assinatura do Solicitante</b></div>",
                        unsafe_allow_html=True,
                    )
                    col_ass2.markdown(
                        "<div style='text-align: center;'>_______________________________________<br><b>Assinatura do Técnico (N1/N2)</b></div>",
                        unsafe_allow_html=True,
                    )

                st.success(
                    "💡 **Dica:** Pressione `Ctrl + P` para salvar como PDF ou imprimir."
                )
    else:
        st.info("📭 Nenhum chamado registrado no banco de dados ainda.")