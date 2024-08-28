import streamlit as st
from PIL import Image

# Configurações da página
st.set_page_config(
    page_title="Página Inicial",
    page_icon="🏚",
    layout="centered"
)

# Cabeçalho
st.title("Página Inicial")
st.image("https://simulare.com.br/wp-content/uploads/SIC.png", use_column_width=True)

# Introdução
st.subheader("Seja muito bem-vindo! Aqui na página inicial você pode conferir muitas dicas e informações:")

# Informação destaque
col1, col2 = st.columns([2, 1])
with col1:
    st.image("https://s2-g1.glbimg.com/7h1jVbkyYev4iyP1Sncz5FYAAIw=/0x0:1700x1065/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2024/9/0/TOMfISRNyrkdHBADI9lA/imagem-g1-8-.jpg", use_column_width=True)
with col2:
    st.write("""
    **O estado de Goiás ficou em primeiro lugar como o estado com maior acesso e desenvolvimento em tecnologia do Brasil.**
    
    Estamos desenvolvendo cada vez mais a possibilidade de acesso para as novas gerações.
    """)
    st.write("Esse sistema pode parecer simples, mas pode ser muito eficaz.")

# Definir URLs
whatsapp_url = "https://wa.me/5562992508093"
localizacao_url = "https://maps.app.goo.gl/VnsF21sL5QJhBEis8"

# Seção de contato
st.markdown("---")
st.subheader("Entre em contato conosco")
st.write("Para saber mais informações de como adquirir esse programa, entre em contato conosco via WhatsApp ou venha nos fazer uma visita!")

# Ícones de contato em colunas
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"[![WhatsApp](https://image.pngaaa.com/345/2169345-middle.png)]({whatsapp_url})")
    st.write("**Atendimento rápido e eficaz via WhatsApp**")

with col2:
    st.markdown(f"[![Localização](https://image.pngaaa.com/627/2173627-middle.png)]({localizacao_url})")
    st.write("**Visite-nos: Rua RI 15 Qd 45, Setor Residencial Itaipu**")

# Footer
st.markdown("---")
st.write("© 2024 Sua Empresa - Todos os direitos reservados.")











