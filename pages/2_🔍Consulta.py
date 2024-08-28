import streamlit as st
import pandas as pd
from datetime import datetime, date

# Definindo o usuário e senha para a área restrita
USERNAME = "admin"
PASSWORD = "admin123"

# Função para verificar login
def check_login(username, password):
    return username == USERNAME and password == PASSWORD

# Página de login
def login():
    st.title("Área Restrita - Login")
    st.text_input("Usuário", key="username")
    st.text_input("Senha", type="password", key="password")
    if st.button("Entrar"):
        if check_login(st.session_state.username, st.session_state.password):
            st.session_state.logged_in = True
            st.success("Login realizado com sucesso!", icon="✅")
        else:
            st.error("Usuário ou senha incorretos", icon="❌")

# Verifica se o usuário está logado
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    # Carrega os dados
    dados = pd.read_csv("clientes.csv")

    # Garantir a ordem das colunas
    colunas_ordenadas = ['nome', 'telefone', 'cpf', 'cnpj', 'dt_contrato', 'tipo', 'valor', 'contrato', 'prazo_contrato']
    dados = dados[colunas_ordenadas]

    st.set_page_config(
        page_title="Consulta cadastro",
        page_icon="🔍"
    )

    st.title("Clientes cadastrados")
    st.divider()

    localizar = st.text_input("Digite o nome", key="localizar")

    # Botões de pesquisa, exclusão e geração de PDF
    col1, col2, col3 = st.columns(3)
    btn_pesquisar = col1.button("Pesquisar", key="Pesquisa")
    btn_excluir = col2.button("Excluir", key="Excluir")

    # Inicializa a variável dados_filtrados
    dados_filtrados = pd.DataFrame()
    
    # Executa a pesquisa quando o botão "Pesquisar" é clicado
    if btn_pesquisar:
        # Filtra os dados com base no nome digitado
        dados_filtrados = dados[dados['nome'].str.contains(localizar, case=False, na=False)]
        
        # Verifica se encontrou algum cliente
        if not dados_filtrados.empty:
            # Calcular o prazo restante ou vencido
            dados_filtrados['prazo_contrato'] = pd.to_datetime(dados_filtrados['prazo_contrato'], format='%Y-%m-%d')
            dados_filtrados['prazo_restante'] = dados_filtrados['prazo_contrato'] - pd.Timestamp(date.today())
            dados_filtrados['prazo_restante'] = dados_filtrados['prazo_restante'].apply(lambda x: f"{x.days} dias" if x.days >= 0 else "Vencido")
            
            # Exibir dados do cliente com prazo
            st.dataframe(dados_filtrados)
            st.success("Cliente encontrado", icon="✅")

            # Verifica se há contratos vencidos
            contratos_vencidos = dados_filtrados[dados_filtrados['prazo_restante'] == "Vencido"]
            if not contratos_vencidos.empty:
                st.warning("Atenção! Este cliente possui contratos vencidos!", icon="⚠️")
        else:
            st.error("Cliente não encontrado", icon="❌")

    # Executa a exclusão quando o botão "Excluir" é clicado
    if btn_excluir:
        # Filtra os dados com base no nome digitado
        dados_filtrados = dados[dados['nome'].str.contains(localizar, case=False, na=False)]
        
        # Verifica se encontrou algum cliente para excluir
        if not dados_filtrados.empty:
            # Exclui o cliente dos dados
            dados = dados[~dados['nome'].str.contains(localizar, case=False, na=False)]
            
            # Salva os dados atualizados de volta ao arquivo CSV
            dados.to_csv("clientes.csv", index=False)
            
            st.success("Cliente excluído com sucesso", icon="✅")
        else:
            st.error("Cliente não encontrado para exclusão", icon="❌")








