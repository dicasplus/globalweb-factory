import streamlit as st

from app.ai_agent import AgenteAtendimento
from app.database import DatabaseManager
from app.pessoas import GerenciadorPessoas, Pessoa
from app.portfolios import GerenciadorPortfolios

# ==============================================================================
# 🔹 CONFIGURAÇÕES INICIAIS DA APLICAÇÃO
# ==============================================================================
st.set_page_config(
    page_title="GLOBAL WEB FACTORY", page_icon=":robot_face:", layout="wide"
)

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

        # Cartões de Resumo das Funcionalidades
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"""
            ### 👥 Seus Dados de Acesso
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
    st.title("Pessoas Cadastradas")
    st.write(
        "Visualização completa da equipe cadastrada no banco de dados."
    )

    # 🟢 Puxa os colaboradores diretamente do SQLite
    pessoas_banco = st.session_state.db.listar_pessoas()

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
                "projeto": "Projetos Atribuídos",
                "senha": None,  # Oculta a senha da tabela por segurança
            },
            hide_index=True,
        )
    else:
        st.info("Nenhuma pessoa encontrada no banco de dados.")

# ------------------------------------------------------------------------------
# TELA 2: CADASTRO DE PESSOAS (Com seleção de múltiplos projetos)
# ------------------------------------------------------------------------------
elif menu == "👤 Cadastrar Pessoa":
    st.title("Cadastrar Novo Colaborador")
    st.write(
        "Preencha as informações abaixo para adicionar a pessoa à equipe."
    )

    with st.form("form_cadastro_pessoa"):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome Completo")
            cargo = st.text_input("Cargo")
            email = st.text_input("E-mail")
            telefone = st.text_input("Telefone / Celular")

        with col2:
            data_admissao = st.text_input("Data Admissão (ex: 01/08/2026)")

            # 🟢 [PARTE 1] Permite selecionar múltiplos projetos para o mesmo usuário
            projetos_selecionados = st.multiselect(
                "Projetos / Contratos de Atuação",
                ["MCTI", "MEC", "COPASA", "Globalweb", "Start Caoa"],
                default=["MCTI"],
            )
            senha = st.text_input("Senha de acesso", type="password")

        btn_salvar = st.form_submit_button("Cadastrar Colaborador")

        if btn_salvar:
            if nome and email and projetos_selecionados:
                # Converte a lista selecionada em texto separado por vírgula
                string_projetos = ", ".join(projetos_selecionados)
                nova_p = Pessoa(
                    nome,
                    cargo,
                    email,
                    telefone,
                    data_admissao,
                    string_projetos,
                    senha,
                )
                st.session_state.gerenciador.adicionar(nova_p)
                st.success(
                    f"✅ Novo Colaborador '{nome}' cadastrado com sucesso nos projetos: **{string_projetos}**!"
                )
            else:
                st.warning(
                    "⚠️ Preencha Nome, E-mail e escolha pelo menos 1 Projeto para continuar."
                )

# ------------------------------------------------------------------------------
# TELA 3: ABERTURA DE CHAMADO (Reativa ao usuário e calculando SLA)
# ------------------------------------------------------------------------------
elif menu == "🎫 Abertura de Chamado":
    st.title("🎫 Abertura Guiada de Chamados")
    st.write("Gere Scripts padronizados de suporte para os portfólios ativos.")

    # 🟢 [PARTE 1] Identificação do Solicitante e Filtro Reativo de Projetos
    pessoas_cadastradas = st.session_state.gerenciador.pessoas

    if pessoas_cadastradas:
        opcoes_pessoas = [
            f"{p.nome} ({p.cargo} | Projetos: {p.projeto})"
            for p in pessoas_cadastradas
        ]
        pessoa_selecionada = st.selectbox(
            "👤 Selecione o Solicitante Cadastrado:",
            options=opcoes_pessoas,
            key="sb_solicitante_chamado",
        )

        idx = opcoes_pessoas.index(pessoa_selecionada)
        objeto_pessoa = pessoas_cadastradas[idx]
        solicitante = objeto_pessoa.nome

        # Extrai somente os projetos em que esta pessoa específica está cadastrada
        projetos_usuario = [
            proj.strip() for proj in objeto_pessoa.projeto.split(",")
        ]
    else:
        st.warning(
            "⚠️ Nenhuma pessoa cadastrada. Usando lista geral de projetos."
        )
        solicitante = st.text_input("Nome do Solicitante", value="Charles")
        projetos_usuario = gerenciador_port.contratos

    st.markdown("---")

    # 🏢 1. Seleção do Projeto (Filtrado reativamente pelos projetos do usuário!)
    proj_escolhido = st.selectbox(
        "Selecione o Projeto do Chamado",
        projetos_usuario,
        key="sb_projeto_atendimento",
    )

    # ⚡ SEÇÃO DE IA: Auto-Categorização por Texto Livre
    with st.expander(
        "✨ Preenchimento Inteligente com IA (Opcional)", expanded=True
    ):
        relato_bruto = st.text_area(
            "Descreva o problema ou necessidade em texto livre:",
            placeholder="Ex: A impressora do 4º andar do MCTI parou de funcionar e está dando erro de rede.",
            key="input_relato_ia",
        )
        if st.button("🤖 Analisar e Preencher Campos com IA"):
            if relato_bruto.strip():
                sugestao = agent_ai.classificar_chamado(
                    relato_bruto,
                    gerenciador_port.contratos,
                    gerenciador_port.categorias_tecnicas,
                )
                if sugestao:
                    st.session_state["sb_categoria_atendimento"] = sugestao.get(
                        "categoria"
                    )
                    st.session_state["sb_subcategoria_atendimento"] = (
                        sugestao.get("subcategoria")
                    )

                    st.success(
                        f"💡 **IA sugeriu:** {sugestao.get('justificativa', 'Análise concluída!')}"
                    )
                    st.info(
                        f"📋 **Sugestão:** {sugestao.get('contrato')} ➔ {sugestao.get('categoria')} ➔ {sugestao.get('subcategoria')}"
                    )
            else:
                st.warning(
                    "⚠️ Digite uma descrição do problema antes de chamar a IA."
                )

    st.markdown("---")

    # 📁 2. Seleção de Categoria e Subcategoria
    categorias = list(gerenciador_port.categorias_tecnicas.keys())
    cat_escolhida = st.selectbox(
        "Selecione a Categoria", categorias, key="sb_categoria_atendimento"
    )

    subcategorias = gerenciador_port.categorias_tecnicas.get(
        cat_escolhida, ["Outros"]
    )
    subcat_escolhida = st.selectbox(
        "Selecione a Subcategoria",
        subcategorias,
        key="sb_subcategoria_atendimento",
    )

    # ⚡ [PARTE 1] Seleção de Impacto & Regra Automática de SLA
    col_imp, col_sla = st.columns(2)
    with col_imp:
        impacto_escolhido = st.select_slider(
            "Impacto da Demanda no Trabalho",
            options=["Baixo", "Médio", "Alto"],
            value="Baixo",
            key="sel_impacto",
        )

    # Regra de Negócio de SLA
    regras_sla = {"Alto": "02 horas", "Médio": "08 horas", "Baixo": "24 horas"}
    prazo_sla_calculado = regras_sla.get(impacto_escolhido, "24 horas")

    with col_sla:
        st.info(f"⏱️ **SLA Previsto de Atendimento:** {prazo_sla_calculado}")

    resumo = st.text_input("Resumo Curto da Demanda")

    # 🏢 3. Campos de Infraestrutura
    col_pat, col_sala, col_ip = st.columns(3)
    with col_pat:
        patrimonio = st.text_input(
            "Número do Patrimônio/EST", key="input_patrimonio"
        )
    with col_sala:
        andar_sala = st.text_input("Andar / Sala", key="input_andar_sala")
    with col_ip:
        endereco_ip = st.text_input(
            "Endereço IP (opcional)", key="input_ip_maquina"
        )

    st.markdown("---")

    # 🪄 4. Polidor Técnico com IA
    st.markdown("### 📝 Detalhamento para o Suporte Técnico")
    if st.button("🪄 Polir e Padronizar Texto com IA"):
        if relato_bruto.strip():
            texto_formatado = agent_ai.polir_descricao(
                texto_bruto=relato_bruto,
                categoria=cat_escolhida,
                subcategoria=subcat_escolhida,
            )
            st.session_state["texto_descricao_polida"] = texto_formatado
            st.success("✨ Texto padronizado e checklist gerado com sucesso!")
        else:
            st.warning("⚠️ Escreva algo no relato inicial para poder polir.")

    descricao_final = st.text_area(
        "Descrição Técnica Final (Editável):",
        value=st.session_state.get("texto_descricao_polida", relato_bruto),
        height=180,
        key="ta_descricao_final",
    )

    st.markdown("---")

    # 🚀 [PARTE 1] Botão de Registro com Geração de Protocolo Formatado
    if st.button("🚀 Criar e Registrar Chamado", type="primary"):
        if resumo.strip() and descricao_final.strip():
            # Gera protocolo amigável no padrão PROJETO-2026-000X
            proximo_id = st.session_state.db.obter_proximo_id()
            protocolo_gerado = f"{proj_escolhido}-2026-{proximo_id:04d}"

            novo_chamado = {
                "protocolo": protocolo_gerado,
                "solicitante": solicitante,
                "projeto": proj_escolhido,
                "categoria": cat_escolhida,
                "subcategoria": subcat_escolhida,
                "resumo": resumo,
                "patrimonio": patrimonio,
                "andar_sala": andar_sala,
                "ip": endereco_ip,
                "descricao": descricao_final,
                "impacto": impacto_escolhido,
                "prazo_sla": prazo_sla_calculado,
            }

            # Salva no Banco de Dados SQLite
            st.session_state.db.salvar_chamado(novo_chamado)

            st.balloons()
            st.success(
                f"✅ **Chamado {protocolo_gerado} registrado com sucesso para {solicitante}! (SLA: {prazo_sla_calculado})**"
            )
        else:
            st.error(
                "❌ Preencha pelo menos o Resumo Curto e a Descrição Técnica para abrir o chamado."
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