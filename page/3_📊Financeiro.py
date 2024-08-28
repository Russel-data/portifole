import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import base64

# Dados de login: usuários e senhas
USER_CREDENTIALS = {
    "admin": "admin123",
    "user1": "mypassword",
    "user2": "streamlit"
}

# Função para verificar o login
def check_login(username, password):
    return USER_CREDENTIALS.get(username) == password

# Função para gerar e baixar PDF consolidado
def gerar_pdf(data, resumo, receita_total, receita_media, crescimento):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Relatório Financeiro Consolidado", ln=True, align='C')
    pdf.ln(10)

    # Seção de Faturamento
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Faturamento ao Longo do Tempo", ln=True)
    pdf.ln(5)
    for index, row in data.iterrows():
        pdf.cell(200, 10, txt=f"{row['dt_contrato'].strftime('%d/%m/%Y')}: R$ {row['valor']:.2f}", ln=True)
    
    # Espaço
    pdf.ln(10)

    # Seção de Análise de Dados
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Análise de Dados", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Receita Total: R$ {receita_total:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Receita Média por Transação: R$ {receita_media:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Crescimento: {crescimento:.2f}%", ln=True)
    
    # Espaço
    pdf.ln(10)

    # Seção de Relatório Financeiro
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumo Financeiro", ln=True)
    pdf.ln(5)
    for index, row in resumo.iterrows():
        pdf.cell(200, 10, txt=f"{row['tipo']}: R$ {row['valor']:.2f}", ln=True)

    # Salvar o PDF no disco
    pdf_output = 'relatorio_financeiro_consolidado.pdf'
    pdf.output(pdf_output)

    # Leitura do arquivo PDF para fazer download
    with open(pdf_output, "rb") as f:
        pdf_data = f.read()
    b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{pdf_output}">Baixar Relatório PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

# Carregar os dados CSV (sem cache para testes)
def load_data(file):
    data = pd.read_csv(file, on_bad_lines='skip', sep=',')  # Usa ',' como separador padrão
    if 'dt_contrato' in data.columns:
        data['dt_contrato'] = pd.to_datetime(data['dt_contrato'], errors='coerce')  # Converte 'dt_contrato' para datetime
    if 'valor' in data.columns:
        data['valor'] = pd.to_numeric(data['valor'], errors='coerce')  # Garante que 'valor' seja numérico
    return data

# Função de login
def login():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Entrar")

    if login_button:
        if check_login(username, password):
            st.session_state['logged_in'] = True
            st.success("Login bem-sucedido!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos!")

# Verifica se o usuário está logado
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
else:
    # Usar o caminho correto do arquivo no seu sistema
    data_file = 'clientes.csv'
    data = load_data(data_file)

    # Título e descrição
    st.title("Dashboard Financeiro")
    st.write("Este dashboard exibe uma análise financeira baseada nos dados de faturamento.")

    # Adicionar um botão para recarregar os dados
    if st.button('Recarregar Dados'):
        st.experimental_set_query_params(reload=True)  # Alternativa para recarregar a página

    # Menu de navegação
    section = st.sidebar.selectbox("Selecione a Seção", ["Faturamento", "Análise de Dados", "Relatórios Financeiros"])

    # Cálculos compartilhados
    receita_total = data['valor'].sum()
    receita_media = data['valor'].mean()
    crescimento = (data['valor'].iloc[-1] - data['valor'].iloc[0]) / data['valor'].iloc[0] * 100
    resumo = data.groupby('tipo').agg({'valor': 'sum'}).reset_index()

    # Seção de Faturamento
    if section == "Faturamento":
        st.header("Faturamento")
        st.write("Visualize e analise os dados de faturamento.")
        
        # Exibição da Tabela de Dados
        st.dataframe(data)
        
        # Gráfico de Faturamento ao longo do tempo
        faturamento_plot = px.line(data, x='dt_contrato', y='valor', title='Faturamento ao Longo do Tempo')
        st.plotly_chart(faturamento_plot)

    # Seção de Análise de Dados
    elif section == "Análise de Dados":
        st.header("Análise de Dados")
        st.write("KPIs e análises detalhadas dos dados financeiros.")
        
        # KPIs
        st.metric(label="Receita Total", value=f"R$ {receita_total:,.2f}")
        st.metric(label="Receita Média por Transação", value=f"R$ {receita_media:,.2f}")
        st.metric(label="Crescimento", value=f"{crescimento:.2f}%")
        
        # Distribuição das Receitas por Tipo de Contrato
        categoria_plot = px.bar(data, x='tipo', y='valor', title='Receita por Tipo de Contrato')
        st.plotly_chart(categoria_plot)

    # Seção de Relatórios Financeiros
    elif section == "Relatórios Financeiros":
        st.header("Relatórios Financeiros")
        st.write("Gere e exporte relatórios financeiros resumidos.")
        
        # Exibir gráfico de barras
        fig_bar = px.bar(resumo, x='tipo', y='valor', title='Distribuição de Receita por Tipo de Contrato')
        st.plotly_chart(fig_bar)
        
        # Exportação de Relatórios
        if st.button('Exportar para Excel'):
            resumo.to_excel('relatorio_financeiro.xlsx', index=False)
            st.success('Relatório exportado com sucesso!')

        if st.button('Exportar para PDF'):
            gerar_pdf(data, resumo, receita_total, receita_media, crescimento)









