import streamlit as st
import pandas as pd
import pygsheets
import os
import datetime
from streamlit_option_menu import option_menu
from streamlit_javascript import st_javascript
from datetime import datetime
import io
import smtplib
from email.message import EmailMessage
from datetime import datetime
import pytz
def hora_brasil():
    fuso_brasil = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasil).strftime("%d/%m/%Y %H:%M:%S")

# Inicializar session_state
if "cadastros" not in st.session_state:
    st.session_state["cadastros"] = []

# Configuração da página
st.set_page_config(layout="wide")

# Página de boas-vindas
if "inicio" not in st.session_state:
    st.session_state["inicio"] = False

if not st.session_state["inicio"]:
    st.title("SISTEMA DE CONTROLE DE BACKSTOCK")
    if st.button("Iniciar"):
        with st.spinner("Carregando o sistema..."):
            import time
            time.sleep(5)
        st.success("Sistema carregado com sucesso! Vamos para a tela de usuário.")
        time.sleep(3)
        st.session_state["inicio"] = True
        st.rerun()

    st.image("https://f.hellowork.com/media/123957/1440_960/IDLOGISTICSFRANCE_123957_63809226079153822430064462.jpeg", use_container_width=True)
    st.stop()

# Cadastro obrigatório do usuário
if "user" not in st.session_state or not st.session_state["user"]:
    st.session_state["user"] = ""

if not st.session_state["user"]:
    st.title("Cadastro Obrigatório para continuar o acesso")
    st.markdown("""
        <style>
        input {
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

    user = st.text_input("Digite seu usuário:")
    st.write(f"Usuário digitado: {user}")

    if user.strip():
        st.session_state["user"] = user.strip()
        st.success(f"Usuário {user} cadastrado com sucesso!")
        st.rerun()
    else:
        st.warning("Por favor, digite um nome de usuário válido.")

    st.image("https://f.hellowork.com/media/123957/1440_960/IDLOGISTICSFRANCE_123957_63809226079153822430064462.jpeg", use_container_width=True)
    st.stop()

# Menu de navegação
st.markdown("""
    <style>
        .css-1omjdxh {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

selecao = option_menu(
    menu_title="BACKSTOCK",
    options=["Cadastro Bulto", "Tabela", "Home"],
    icons=["box", "table", "house"],
    menu_icon="cast",
    orientation="horizontal"
)

# Redireciona para tela de boas-vindas
if selecao == "Home":
    st.session_state["inicio"] = False
    st.session_state["user"] = ""
    st.session_state["bulto_cadastrado"] = False
    st.rerun()

# Página de cadastro de bultos
if selecao == "Cadastro Bulto":
    st.markdown("<h1 style='color:black;'>Cadastro de Bultos</h1>", unsafe_allow_html=True)

    if "bulto_numero" not in st.session_state:
        st.session_state["bulto_numero"] = ""
        st.session_state["bulto_cadastrado"] = False
    if "peca" not in st.session_state:
        st.session_state["peca"] = ""

    if not st.session_state["bulto_cadastrado"]:
        st.markdown("""
            <style>
                input { color: black !important; }
                ::placeholder { color: lightgray !important; }
                label { color: black !important; }
            </style>
        """, unsafe_allow_html=True)

        bulto = st.text_input("Digite o número do bulto:")
        if bulto:
            st.session_state["bulto_numero"] = bulto
            st.session_state["bulto_cadastrado"] = True
            st.rerun()
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<p style='font-size:25px; color:black;'><b>User:</b> <span style='color:dimgray;'>{st.session_state['user']}</span></p>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<p style='font-size:25px; color:black;'><b>Bulto:</b> <span style='color:dimgray;'>{st.session_state['bulto_numero']}</span></p>", unsafe_allow_html=True)
        with col3:
            total_sku_local = st.session_state.get("peca_reset_count", 0)
            st.markdown(f"<p style='font-size:25px; color:black;'><b>SKU:</b> <span style='color:dimgray;'> {total_sku_local}</p>", unsafe_allow_html=True)

        unique_key = f"peca_{st.session_state.get('peca_reset_count', 0)}"

        st.markdown("""
            <style>
                ::placeholder { color: black !important; }
                .stTextInput > div > div > input { color: black !important; }
                label { color: black !important; }
            </style>
        """, unsafe_allow_html=True)

        categorias = ["Ubicação", "Limpeza", "Tara Maior", "Costura", "Reetiquetagem"]
        if "categoria_selecionada" not in st.session_state:
            st.session_state["categoria_selecionada"] = None

        st.markdown("<h3 style='color:white;'>Escolha uma categoria:</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        for i, categoria in enumerate(categorias):
            col = [col1, col2, col3][i % 3]
            with col:
                if st.button(categoria, key=f"btn_{categoria}", help=f"Selecionar {categoria}", use_container_width=True):
                    st.session_state["categoria_selecionada"] = categoria
                    st.success(f"Categoria '{categoria}' selecionada!")

        sku = st.text_input("Digite SKU para este bulto:", key=unique_key)
        if "ultimo_sku" not in st.session_state:
            st.session_state["ultimo_sku"] = ""

        if sku:
            if not st.session_state.get("bulto_numero"):
                st.warning("Cadastre um bulto antes de cadastrar uma peça.")
            elif not st.session_state.get("categoria_selecionada"):
                st.warning("Selecione uma categoria antes de cadastrar a peça.")
            else:
               # horario_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                novo_cadastro = {
                    "Usuário": st.session_state["user"],
                    "Bulto": st.session_state["bulto_numero"],
                    "SKU": sku,
                    "Categoria": st.session_state["categoria_selecionada"],
                    "Data/Hora": hora_brasil()
                }
                st.session_state["cadastros"].append(novo_cadastro)
                st.success(f"Peça '{sku}' cadastrada no Bulto {st.session_state['bulto_numero']} na categoria '{st.session_state['categoria_selecionada']}'!")
                st.session_state["peca_reset_count"] = st.session_state.get("peca_reset_count", 0) + 1
                st.session_state["ultimo_sku"] = sku
                st.rerun()

        with col2:
            if st.button("Finalizar Bulto"):
                st.success("Bulto finalizado com sucesso!")
                st.session_state["bulto_numero"] = ""
                st.session_state["bulto_cadastrado"] = False
                st.session_state["peca_reset_count"] = 0
                st.rerun()

# Tabela de peças cadastradas
elif selecao == "Tabela":
    st.markdown("<h1 style='color:black;'>Tabela de Peças Cadastradas</h1>", unsafe_allow_html=True)

    if st.session_state["cadastros"]:
        df_cadastros = pd.DataFrame(st.session_state["cadastros"])
        st.dataframe(df_cadastros, use_container_width=True)
        nome_arquivo = f"cadastro_bultos_{datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%d-%m-%Y_%H-%M-%S')}.xlsx"

       # nome_arquivo = f"cadastro_bultos_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.xlsx"
        output = io.BytesIO()
        df_cadastros.to_excel(output, index=False, engine='xlsxwriter')
        dados_excel = output.getvalue()

        st.download_button(
            label="📥 Baixar planilha Excel",
            data=dados_excel,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        if st.button("✉️ Enviar planilha para analista"):
            try:
                remetente = "rogeriomartins1206@gmail.com"
                senha = "zqcpbmisdghscjcv"
                destinatario = "analista@empresa.com"

                msg = EmailMessage()
                msg['Subject'] = 'Relatório de Cadastro de Bultos'
                msg['From'] = remetente
                msg['To'] = destinatario
                msg.set_content('Segue em anexo a planilha de cadastro de bultos.')
                msg.add_attachment(dados_excel, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=nome_arquivo)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(remetente, senha)
                    smtp.send_message(msg)

                st.success("✅ Planilha enviada com sucesso para o analista!")

            except Exception as e:
                st.error(f"❌ Erro ao enviar planilha: {e}")
    else:
        st.info("Nenhuma peça cadastrada até o momento.")

# Rodapé
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            right: 10px;
            font-size: 12px;
            text-align: right;
            background-color: #9DD1F1;
            color: black;
            padding: 5px;
            z-index: 100;
        }
    </style>
    <div class="footer">
        Copyright © 2025 Direitos Autorais Desenvolvedor Rogério Ferreira
    </div>
""", unsafe_allow_html=True)
