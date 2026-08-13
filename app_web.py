import streamlit as st
from streamlit import subheader

from app.pessoas import Pessoa, GerenciadorPessoas
from app.portfolios import GerenciadorPortfolios
from app.portfolios import Chamado
#from main import solicitante, gerenciador

# 1 - Configurações visuais da aba do navegador

st.set_page_config(
    page_title="GLOBAL WEB FACTORY",
    page_icon=":robot_face:",
    layout="wide"
)

# 2 Inicialização da Memória da sessão (Session State)

if 'gerenciador' not in st.session_state:
    st.session_state['gerenciador'] = GerenciadorPessoas()
    # Pessoas iniciais para teste
    p1 = Pessoa("Charles Ferreira de Moura", "Dev Junior", "charles@empresa.com", "61 9999-9999", "01/08/2024", "MCTI",
                "123456")
    p2 = Pessoa("Ana Carolina", "Analista de Dados", "ana@colabaradores.empresa.com", "61 9991-1234", "01/01/2026",
                "MEC", "1234567")
    st.session_state.gerenciador.adicionar(p1)
    st.session_state.gerenciador.adicionar(p2)

    if 'gerenciador_portfolios' not in st.session_state:
        st.session_state.gerenciador_portfolios = GerenciadorPortfolios()

    # Texto temporario só pra testar a primeira subida
    st.title(" Sistema Global Web Factory - Web")
    st.write("A estrutura inicial da memória carregada com sucesso!")

# 3 Barra lateral menu de navegação
# *****************************************

st.sidebar.title("GlobalWeb Factory")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Início",
        "📋 Listar Pessoas",
        "👤 Cadastrar Pessoa",
        "🎫 Abertura de Chamado",
        "📁 Projetos / Portfólios"
    ]
)

#------------------------------------------------------
#       TELA 0: INICIO DA TELA
#-------------------------------------------------------

if menu == "🏠 Início":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Exibe a logo centralizada
        st.image("logo.png", use_container_width=True)

    st.markdown("<h1 style='text-align: center;'>GlobalWeb Factory</h1>  ", unsafe_allow_html=True)
    st.markdown("<h3 style = 'text-aling: center; color:#888;'> Sistema de Integração de Gestão de Equipe e Suporte</h3>  ", unsafe_allow_html=True)

    st.markdown("---")

    #cartoes explicativo dos módulos
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



# TELA 1: LISTAGEM DE PESSOAS
# *********************************

if menu == "📋 Listar Pessoas":
    st.title("Pessass Cadastradas")
    st.write("Visualização completa da equipe e colaboradores do sistema.")

    # Buscar a lista de pessoas salvas no Gerenciador dentro do session_sate
    pessoas = st.session_state.gerenciador.pessoas

    if pessoas:
        dados_tabela = []
        for p in pessoas:
            dados_tabela.append({
                "Nome:": p.nome,
                "Cargo:": p.cargo,
                "E-mail:": p.email,
                "Telefone:": p.telefone,
                "Admissão": p.data_admissao,
                "Projeto:": p.projeto
            })
        # desenhar a tabela interatva na tela web
        st.dataframe(dados_tabela, use_container_width=True)
    else:
        st.info("Nenhuma pessoa encontrada no momento")

elif menu == "Cadastrar Pessoa":
    st.title("Cadastrar Pessoa (Em breve...na etapa 3")

elif menu == "Abertura de Chamado":
    st.title("Abertura de Chamado(em breve na etapa 4)")
elif menu == "Projeto / Portfolios":
    st.title("Projetos / Portfolios (Em breve na etapa 4)")


#tela 2: Cadastro de Pessoas
elif menu == "👤 Cadastrar Pessoa":
    st.title("Cadastrar Novo Colaborador")
    st.write("Preencha as informações abaixo para adicionar a pessoas à Equipe")

    #st.form  cria um bloco unificado. Os dados são enviados ao clicar no botão!
    with st.form("form_cadastro_pessoa"):
        #dividimos a tela em duas colunas para o formulário não ficar muito longo
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome Completo")
            cargo = st.text_input("Cargo")
            email = st.text_input("E-mail")
            telefone = st.text_input("Telefone / Celular")

        with col2:
            data_admissao = st.text_input("Data Admissao (ex: 01/08/2026")
            projeto = st.selectbox("Projeto / Contrato", ["MCTI", "MEC", "COPASA", "Globalweb" ])
            senha = st.text_input("Senha de acesso", type="password")

        btn_salvar = st.form_submit_button("Cadastrar Colaborador")

        #Lógica executada quando é clicada
        if btn_salvar:
            if nome and email:

                #Criamos o objeto Pessoa usando a sua classe existente
                nova_p = Pessoa(nome, cargo, email, telefone, data_admissao, projeto, senha)

                #Guardamos na lista através do gerenciador no sesseion state
                st.session_state.gerenciador.adicionar(nova_p)

                #Feedback visual verde de sucesso
                st.success("Novo Colaborador '{nome}' com sucesso!")
            else:
                #feedback visual amarelo de aviso
                st.warning(" Preencha ao menos o Nome e o E-mail para continuar ")


elif menu == "🎫 Abertura de Chamado":
    st.title("🎫 Abertura Guiada de Chamados")
    st.write("Gere Scripts padronizados de suporte para os porfólios ativos.")

    solicitante = st.text_input(" Nome do Solicitante", value="Charles")

    #Recuéra o gerenciador de portfóçops da memória da sessão
    gerenciador_port = st.session_state.gerenciador_portfolios
    proj_escolhido = st.selectbox("Selecione o Projeto  / contrato", gerenciador_port.contratos)
    categorias = list(gerenciador_port.categorias_tecnicas.keys())
    cat_escolhida = st.selectbox("Selecione a Categoria", categorias)
    subcategorias = gerenciador_port.categorias_tecnicas[cat_escolhida]
    subcat_escolhida = st.selectbox("Selecione a Subcategoria", subcategorias)

    resumo = st.text_input("Resumo Curto da Demanda")

    #Campos dinamicos baseados na categoria escolhida
    detalhes = {}
    if "Equipamento" in cat_escolhida or "Patrimônio" in cat_escolhida:
        detalhes["Código Patrimônio (EST)"] = st.text_input("Número do Patrimônio/EST")
        detalhes["Localização / Andar "] = st.text_input("Andar / Sala")
        detalhes["IP do Host"] = st.text_input("Endereço IP (opcional)")
    else:
        detalhes["Descrição do Problema"] = st.text_area("Detalhe da Necessidade ")
        detalhes["Impacto no trabalho"] = st.select_slider("Impacto no trabalho", options=["Baixo", "Médio", "Crítico"])

    if st.button("🚀 Gerar Ticket Formatado"):
        if resumo:
            from app.portfolios import Chamado
            chamado = Chamado(proj_escolhido, cat_escolhida, subcat_escolhida, solicitante, resumo, detalhes)

            st.markdown("---")
            st.markdown("### 📝 Script Gerado para o Ticket")
            #st.code renderiza um bloco escuro com botão de copiar automatico!
            st.code(chamado.gerar_script_detalhado(), language="text")

        else:
            st.warning("⚠️ Preencha o resumo da demanda antes de gerar o ticket.")

    #tela 4 - PROJETOS  / PORTFOLIOS

    #elif menu == "📁 Projetos / Portfólios":
elif  "Projetos" in menu:
        st.title("📂 Matriz de Portfólios & Contratos ")
        st.caption("Guia de Referência rápida do escopo de atendimento para colaboradores e gestores. ")

        # 1. recupera o gerenciador da sessão antes de usar
        gerenciador_port = st.session_state.gerenciador_portfolios

        # 1. Metricas de Resumo no topo
        col_m1, col_m2, col_m3 = st.columns(3)
        total_contratos = len(gerenciador_port.contratos)
        total_cats = len(gerenciador_port.categorias_tecnicas)
        total_subcats = sum(len(subs) for subs in gerenciador_port.categorias_tecnicas.values())

        col_m1.metric("🏢 Contratos Ativos", total_contratos)
        col_m2.metric("📁 Categorias Principais", total_cats)
        col_m3.metric("📄 Subcategorias Mapeadas", total_subcats)

        st.markdown("---")

        # 2. Visualiação em abas (tabs) para organização
        tab_contratos, tab_esqueleto = st.tabs(["🏢 Contratos & Clientes", "🌳 Esqueleto do Catálogo Técnico"])


        with tab_contratos:
            st.subheader("Lista de Contratos Habilitados")
            st.info("Projetos e empresas atualmente atendidos pela operação")
            for contrato in gerenciador_port.contratos:
                st.markdown(f"- **{contrato}**")

        with tab_esqueleto:
            st.subheader("Árvore de Categorias e Subcategorias")
            st.write("Expanda as categorias para consultar o escopo detalhado de cada área de suporte:")




            for cat, subcats in gerenciador_port.categorias_tecnicas.items():
                with st.expander(f"📁{cat} | ({len(subcats)} Subcategorias)"):
                    for subcat in subcats:
                        st.write(f"- {subcat}")



















