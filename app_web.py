import streamlit as st

from app.ai_agent import AgenteAtendimento
from app.pessoas import GerenciadorPessoas, Pessoa
from app.portfolios import GerenciadorPortfolios
from app.database import DatabaseManager

# 1 - Configurações visuais da aba do navegador
st.set_page_config(
    page_title="GLOBAL WEB FACTORY", page_icon=":robot_face:", layout="wide"
)

# 2 - Inicialização da Memória da sessão (Session State)
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
        "MCTI",
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


# 3 - Barra lateral / Menu de navegação
st.sidebar.title("GlobalWeb Factory")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Início",
        "📋 Listar Pessoas",
        "👤 Cadastrar Pessoa",
        "🎫 Abertura de Chamado",
        "📊 Histórico de Chamados",
        "📁 Projetos / Portfólios",
    ],
)

# ----------------------------------------------------------------------
# TELA 0: INÍCIO
# ----------------------------------------------------------------------
if menu == "🏠 Início":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_container_width=True)

    st.markdown(
        "<h1 style='text-align: center;'>GlobalWeb Factory</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align: center; color:#888;'>Sistema de Integração de Gestão de Equipe e Suporte</h3>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.info("""
        ### 👥 Gestão de Colaboradores
        * **Listagem:** Acesso à base completa de colaboradores ativos.
        * **Cadastro:** Formulário estruturado para novos membros da equipe.
        """)

    with c2:
        st.success("""
        ### 🎫 Suporte & Portfólios
        * **Chamados Guiados:** Padronização e geração de tickets.
        * **Catálogo:** Visão geral de contratos e categorias ativas.
        """)

    st.markdown("---")
    st.caption("🚀 **Desenvolvido por Charles** | Python 3 & Streamlit")

# ----------------------------------------------------------------------
# TELA 1: LISTAGEM DE PESSOAS
# ----------------------------------------------------------------------
elif menu == "📋 Listar Pessoas":
    st.title("Pessoas Cadastradas")
    st.write("Visualização completa da equipe e colaboradores do sistema.")

    pessoas = st.session_state.gerenciador.pessoas

    if pessoas:
        dados_tabela = []
        for p in pessoas:
            dados_tabela.append({
                "Nome": p.nome,
                "Cargo": p.cargo,
                "E-mail": p.email,
                "Telefone": p.telefone,
                "Admissão": p.data_admissao,
                "Projeto": p.projeto,
            })
        st.dataframe(dados_tabela, use_container_width=True)
    else:
        st.info("Nenhuma pessoa encontrada no momento.")

# ----------------------------------------------------------------------
# TELA 2: CADASTRO DE PESSOAS
# ----------------------------------------------------------------------
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
            projeto = st.selectbox(
                "Projeto / Contrato", ["MCTI", "MEC", "COPASA", "Globalweb"]
            )
            senha = st.text_input("Senha de acesso", type="password")

        btn_salvar = st.form_submit_button("Cadastrar Colaborador")

        if btn_salvar:
            if nome and email:
                nova_p = Pessoa(
                    nome, cargo, email, telefone, data_admissao, projeto, senha
                )
                st.session_state.gerenciador.adicionar(nova_p)
                st.success(f"Novo Colaborador '{nome}' cadastrado com sucesso!")
            else:
                st.warning("Preencha ao menos o Nome e o E-mail para continuar.")

# ----------------------------------------------------------------------
# TELA 3: ABERTURA DE CHAMADO
# ----------------------------------------------------------------------
elif menu == "🎫 Abertura de Chamado":
    st.title("🎫 Abertura Guiada de Chamados")
    st.write("Gere Scripts padronizados de suporte para os portfólios ativos.")

    #solicitante = st.text_input("Nome do Solicitante", value="Charles")
    # ----------------------------------------------------------------------
    # 👤 IDENTIFICAÇÃO DO SOLICITANTE (Busca na Base Cadastrada)
    # ----------------------------------------------------------------------
    pessoas_cadastradas = st.session_state.gerenciador.pessoas

    if pessoas_cadastradas:
        # Cria uma lista formatada com Nome + Cargo para facilitar a seleção
        opcoes_pessoas = [
            f"{p.nome} ({p.cargo} - {p.projeto})" for p in pessoas_cadastradas
        ]
        pessoa_selecionada = st.selectbox(
            "👤 Selecione o Solicitante Cadastrado:",
            options=opcoes_pessoas,
            key="sb_solicitante_chamado",
        )

        # Extrai o objeto da pessoa selecionada para vincular ao chamado
        idx = opcoes_pessoas.index(pessoa_selecionada)
        objeto_pessoa = pessoas_cadastradas[idx]
        solicitante = objeto_pessoa.nome
    else:
        st.warning(
            "⚠️ Nenhuma pessoa cadastrada na base. Cadastre colaboradores na aba '👤 Cadastrar Pessoa'."
        )
        solicitante = st.text_input("Nome do Solicitante (Manual)")

    gerenciador_port = st.session_state.gerenciador_portfolios
    agent_ai = st.session_state.agent_ai

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
                    st.session_state["sb_projeto_atendimento"] = sugestao.get(
                        "contrato"
                    )
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

    # 🟢 Caixas de Seleção Reativas (Fora do Expander)
    proj_escolhido = st.selectbox(
        "Selecione o Projeto / Contrato",
        gerenciador_port.contratos,
        key="sb_projeto_atendimento",
    )

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

    resumo = st.text_input("Resumo Curto da Demanda")

    # 🏢 CAMPOS DE INFRAESTRUTURA E LOCALIZAÇÃO
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

    # 🪄 POLIDOR TÉCNICO E DETALHAMENTO DA DEMANDA
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

    # 🚀 BOTÃO ÚNICO DE CRIAÇÃO E ENVIO DO TICKET
    # 🚀 BOTÃO ÚNICO DE CRIAÇÃO E ENVIO DO TICKET
    if st.button("🚀 Criar e Registrar Chamado", type="primary"):
        if resumo.strip() and descricao_final.strip():
            novo_chamado = {
                "solicitante": solicitante,
                "projeto": proj_escolhido,
                "categoria": cat_escolhida,
                "subcategoria": subcat_escolhida,
                "resumo": resumo,
                "patrimonio": patrimonio,
                "andar_sala": andar_sala,
                "ip": endereco_ip,
                "descricao": descricao_final,
                "impacto": st.session_state.get("sel_impacto", "Baixo"),
            }

            # 🟢 MÁGICA ACONTECENDO: Salvando no Banco de Dados SQLite!
            id_chamado = st.session_state.db.salvar_chamado(novo_chamado)

            st.balloons()
            st.success(
                f"✅ **Chamado #{id_chamado} registrado com sucesso para {solicitante}!**"
            )
            # st.json(novo_chamado) # Opcional: pode comentar ou apagar se não quiser mostrar o JSON na tela
        else:
            st.error(
                "❌ Preencha pelo menos o Resumo Curto e a Descrição Técnica para abrir o chamado."
            )

# ----------------------------------------------------------------------
# TELA 4: PROJETOS / PORTFÓLIOS
# ----------------------------------------------------------------------
elif menu == "📁 Projetos / Portfólios":
    st.title("📂 Matriz de Portfólios & Contratos")
    st.caption(
        "Guia de Referência rápida do escopo de atendimento para colaboradores e gestores."
    )

    gerenciador_port = st.session_state.gerenciador_portfolios

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

# ----------------------------------------------------------------------
# TELA 5: PAINEL DE HISTÓRICO DE CHAMADOS
# ----------------------------------------------------------------------
elif menu == "📊 Histórico de Chamados":
    st.title("📊 Painel de Chamados Registrados")
    st.write("Acompanhe o histórico de todas as solicitações salvas no banco de dados.")

    # Puxa os dados direto do SQLite
    chamados_salvos = st.session_state.db.listar_chamados()

    if chamados_salvos:
        # 1. 📈 Criar Métricas Resumidas no Topo
        total_chamados = len(chamados_salvos)
        chamados_altos = len([c for c in chamados_salvos if c.get("impacto") == "Alto"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Chamados Abertos", total_chamados)
        col2.metric("Chamados de Alto Impacto", chamados_altos)
        col3.metric("Status do Banco", "Online 🟢")

        st.markdown("---")
        st.subheader("📋 Tabela de Registros")

        # 2. 🗂️ Exibir a Tabela de Dados Formatada
        st.dataframe(
            chamados_salvos,
            use_container_width=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", format="#%d"),
                "data_abertura": st.column_config.DatetimeColumn("Abertura", format="DD/MM/YYYY HH:mm"),
                "solicitante": "Solicitante",
                "projeto": "Contrato",
                "categoria": "Categoria",
                "subcategoria": "Subcategoria",
                "resumo": "Resumo",
                "impacto": "Impacto",
                # Ocultando colunas que poluem muito a tabela (mas continuam no banco!)
                "descricao": None,
                "patrimonio": None,
                "andar_sala": None,
                "ip": None
            },
            hide_index=True  # Esconde aquele índice numérico extra do lado esquerdo
        )
        # ----------------------------------------------------------------------
        # 🖨️ ÁREA DE VISUALIZAÇÃO E IMPRESSÃO DE ORDEM DE SERVIÇO
        # ----------------------------------------------------------------------
        st.markdown("---")
        st.subheader("🖨️ Visualizar e Imprimir Chamado")

        # Cria uma lista amigável para o menu de seleção
        opcoes_chamados = ["Selecione um chamado..."] + [
            f"Chamado #{c['id']} - {c['projeto']} ({c['resumo']})"
            for c in chamados_salvos
        ]

        chamado_selecionado = st.selectbox("Selecione para gerar a Ordem de Serviço:", opcoes_chamados)

        if chamado_selecionado != "Selecione um chamado...":
            # Extrai o ID do texto selecionado (Ex: "Chamado #2 - ..." -> pega o 2)
            id_selecionado = int(chamado_selecionado.split("#")[1].split(" -")[0])

            # Localiza os dados completos do chamado no banco
            ticket = next((c for c in chamados_salvos if c["id"] == id_selecionado), None)

            if ticket:
                # 🟢 CSS MÁGICO PARA IMPRESSÃO (Ctrl+P)
                # Esconde menus e botões na hora de imprimir para ficar limpo
                st.markdown("""
                            <style>
                            @media print {
                                section[data-testid="stSidebar"] {display: none !important;}
                                header[data-testid="stHeader"] {display: none !important;}
                                .stSelectbox {display: none !important;}
                                button {display: none !important;}
                                .main .block-container {max-width: 100% !important; padding: 1rem !important;}
                            }
                            </style>
                        """, unsafe_allow_html=True)

                # 📇 LAYOUT DA ORDEM DE SERVIÇO (Pronto para PDF/Impressora)
                with st.container(border=True):
                    col_logo, col_titulo = st.columns([1, 4])
                    with col_logo:
                        st.image("logo.png", width=100)  # Reutiliza sua logo
                    with col_titulo:
                        st.markdown(f"## 🎫 Ordem de Serviço de TI - #{ticket['id']}")
                        st.caption(f"**Data de Abertura:** {ticket['data_abertura']}")

                    st.markdown("---")

                    # Metadados em colunas
                    c1, c2, c3, c4 = st.columns(4)
                    c1.markdown(f"**👤 Solicitante:**\n{ticket['solicitante']}")
                    c2.markdown(f"**🏢 Contrato:**\n{ticket['projeto']}")
                    c3.markdown(f"**📁 Categoria:**\n{ticket['categoria']}")
                    c4.markdown(f"**⚠️ Impacto:**\n{ticket['impacto']}")

                    # Informações de Infraestrutura (só mostra se tiver preenchido)
                    if ticket['patrimonio'] or ticket['andar_sala'] or ticket['ip']:
                        st.markdown("<br>", unsafe_allow_html=True)
                        c_infra1, c_infra2, c_infra3 = st.columns(3)
                        c_infra1.markdown(f"**🖥️ Patrimônio:** {ticket['patrimonio'] or 'N/A'}")
                        c_infra2.markdown(f"**📍 Localização:** {ticket['andar_sala'] or 'N/A'}")
                        c_infra3.markdown(f"**🌐 Endereço IP:** {ticket['ip'] or 'N/A'}")

                    st.markdown("---")

                    # Descrição Técnica
                    st.markdown("### 📝 Descrição Técnica e Diagnóstico")
                    st.info(f"**Resumo:** {ticket['resumo']}")
                    st.markdown(ticket['descricao'])  # Como a IA gera Markdown, vai ficar formatado perfeitinho!

                    st.markdown("---")

                    # Área de Assinatura para impressão física
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    col_ass1, col_ass2 = st.columns(2)
                    col_ass1.markdown(
                        "<div style='text-align: center;'>_______________________________________<br><b>Assinatura do Solicitante</b></div>",
                        unsafe_allow_html=True)
                    col_ass2.markdown(
                        "<div style='text-align: center;'>_______________________________________<br><b>Assinatura do Técnico (N1/N2)</b></div>",
                        unsafe_allow_html=True)

                st.success(
                    "💡 **Dica:** Pressione `Ctrl + P` no teclado para salvar esta Ordem de Serviço como PDF ou imprimir. O menu lateral desaparecerá automaticamente na impressão!")
    else:
        st.info("📭 Nenhum chamado registrado no banco de dados ainda. Abra um chamado para testar!")