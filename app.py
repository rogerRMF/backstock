import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu
import urllib.parse

# Configuração da página
st.set_page_config(layout="wide")

# Inicializar session_state para controle de dados
if "dados" not in st.session_state:
    st.session_state["dados"] = pd.DataFrame(columns=["Bulto", "Sku", "Categoria", "Data/Hora", "Usuario"])
if "inicio" not in st.session_state:
    st.session_state["inicio"] = False
if "user" not in st.session_state:
    st.session_state["user"] = ""

# Página de boas-vindas
if not st.session_state["inicio"]:
    st.title("SISTEMA DE CONTROLE DE BACKSTOCK")
    if st.button("Iniciar"):
        st.session_state["inicio"] = True
        st.rerun()
    st.stop()

# Cadastro de usuário
if not st.session_state["user"]:
    st.title("Cadastro Obrigatório")
    user = st.text_input("Digite seu usuário:")
    if user.strip():
        st.session_state["user"] = user.strip()
        st.success(f"Usuário {user} cadastrado com sucesso!")
        st.rerun()
    st.stop()

# Menu de navegação
selecao = option_menu(
    menu_title="BACKSTOCK",
    options=["Cadastro Bulto", "Tabela", "Enviar WhatsApp", "Home"],
    icons=["box", "table", "whatsapp", "house"],
    menu_icon="cast",
    orientation="horizontal"
)

# Cadastro de Bulto
if selecao == "Cadastro Bulto":
    st.title("Cadastro de Bultos")
    bulto = st.number_input("Digite o número do bulto:", min_value=1, step=1)
    sku = st.text_input("Digite SKU para este bulto:")
    categorias = ["Ubicação", "Limpeza", "Tara Maior", "Costura", "Reetiquetagem"]
    categoria = st.selectbox("Escolha uma categoria:", categorias)
    
    if st.button("Cadastrar Peça"):
        if bulto and sku and categoria:
            nova_linha = pd.DataFrame({
                "Bulto": [bulto],
                "Sku": [sku],
                "Categoria": [categoria],
                "Data/Hora": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "Usuario": [st.session_state["user"]]
            })
            st.session_state["dados"] = pd.concat([st.session_state["dados"], nova_linha], ignore_index=True)
            st.success("Peça cadastrada com sucesso!")
        else:
            st.warning("Preencha todos os campos antes de cadastrar.")

elif selecao == "Tabela":
    st.title("Tabela de Dados")
    st.dataframe(st.session_state["dados"])

elif selecao == "Enviar WhatsApp":
    st.title("Enviar Dados via WhatsApp")
    if not st.session_state["dados"].empty:
        numero = st.text_input("Digite o número do WhatsApp (com DDD e sem espaços):")
        if st.button("Enviar") and numero:
            tabela = st.session_state["dados"].to_string(index=False)
            mensagem = f"Dados do Backstock:\n{tabela}"
            url = f"https://api.whatsapp.com/send?phone={numero}&text={urllib.parse.quote(mensagem)}"
            st.markdown(f"[Clique aqui para enviar pelo WhatsApp]({url})", unsafe_allow_html=True)
    else:
        st.warning("Nenhum dado para enviar.")

elif selecao == "Home":
    st.session_state["inicio"] = False
    st.session_state["user"] = ""
    st.rerun()
