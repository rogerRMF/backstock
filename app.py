import streamlit as st
import pandas as pd
import pygsheets
from streamlit_gsheets import GSheetsConnection
import os
import datetime
from streamlit_option_menu import option_menu
from streamlit_javascript import st_javascript
from datetime import datetime 
import json
import streamlit as st
import pygsheets
import json

# Verificar se o Streamlit tem as credenciais carregadas
if "google" not in st.secrets:
    st.error("🚨 Credenciais do Google não encontradas! Verifique o secrets.toml.")
    st.stop()

# Criar credenciais com os dados do Streamlit Secrets
credenciais = {
    "type": st.secrets["google"]["type"],
    "project_id": st.secrets["google"]["project_id"],
    "private_key_id": st.secrets["google"]["private_key_id"],
    "private_key": st.secrets["google"]["private_key"].replace(" ", "\n"),  # Corrigir o formato da chave
    "client_email": st.secrets["google"]["client_email"],
    "client_id": st.secrets["google"]["client_id"],
    "auth_uri": st.secrets["google"]["auth_uri"],
    "token_uri": st.secrets["google"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["google"]["client_x509_cert_url"],
}





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

# Inicializar session_state para controle do usuário
if "user" not in st.session_state or not st.session_state["user"]:
    st.session_state["user"] = ""

# Página de cadastro obrigatório do usuário antes de acessar o sistema
if not st.session_state["user"]:
    st.title("Cadastro Obrigatório para continuar o acesso")
    st.markdown(
    """
    <style>
    input {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

    st.markdown(
       """
        <style>
           .css-1omjdxh {
              color: white !important;
        }
       </style>
       """,
    unsafe_allow_html=True
)
selecao = option_menu(
    menu_title="BACKSTOCK",
    options=["Cadastro Bulto", "Tabela", "Home"],
    icons=["box", "table", "dash", "house"],
    menu_icon="cast",
    orientation="horizontal"
)


# Autorizar acesso ao Google Sheets
credenciais = pygsheets.authorize(service_file=os.path.join(os.getcwd(), "cred.json"))
meuArquivoGoogleSheets = "https://docs.google.com/spreadsheets/d/1SFModXntK_P68nyofSYiB636eKG_uSZc_-f-mvWP1Yc/"
arquivo = credenciais.open_by_url(meuArquivoGoogleSheets)
aba = arquivo.worksheet_by_title("backstock")

# Carregar os dados da planilha e remover colunas vazias
data = aba.get_all_values()
if data:
    df = pd.DataFrame(data[1:], columns=data[0])  # Cria DataFrame com cabeçalho correto
    df = df.loc[:, ~df.columns.duplicated()]  # Remove colunas duplicadas
    df = df.dropna(axis=1, how="all")  # Remove colunas completamente vazias
else:
    df = pd.DataFrame(columns=["Bulto", "Sku", "Categoria", "Data/Hora", "Usuario"])

# Função para salvar dados no Google Sheets
def salvar_dados_no_sheets(bulto, sku, categoria, Usuario):
  # data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   # data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_hora = datetime.now().strftime("%Y-%m-%d")

# Obtém data e hora atual
    nova_linha = [bulto, sku, categoria, data_hora, Usuario]
    aba.append_table(values=[nova_linha], start="A1", dimension="ROWS", overwrite=False)

# Configuração das telas
if selecao == "Cadastro Bulto":
    st.markdown("<h1 style='color:black;'>Cadastro de Bultos</h1>", unsafe_allow_html=True)


    if "bulto_numero" not in st.session_state:
        st.session_state["bulto_numero"] = ""
        st.session_state["bulto_cadastrado"] = False
    if "peca" not in st.session_state:
        st.session_state["peca"] = ""
    
    if not st.session_state["bulto_cadastrado"]:
        st.markdown(
    """
    <style>
        /* Muda a cor do texto digitado no input para branco */
        input {
            color: black !important;
        }
        
        /* Opcional: Mudar a cor do placeholder para cinza claro */
        ::placeholder {
            color: lightgray !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
        st.markdown(
    """
    <style>
        /* Muda a cor do texto do label para branco */
        label {
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

        bulto = st.number_input("Digite o número do bulto:", min_value=0, step=1,  format="%d")
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
            total_sku_local = st.session_state.get("peca_reset_count", 0)  # Contador local
            st.markdown(f"<p style='font-size:25px; color:black;'><b>SKU:</b> <span style='color:dimgray;'> {total_sku_local}</p>", unsafe_allow_html=True)

        unique_key = f"peca_{st.session_state.get('peca_reset_count', 0)}"
                        
        st.markdown(
    """
    
    <style>
        /* Estiliza o placeholder (texto dentro do input antes de digitar) */
        ::placeholder { 
            color: black !important;
        }

        /* Estiliza o input para garantir que o texto digitado também fique branco */
        .stTextInput > div > div > input {
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
        
        
        st.markdown(
    """
    <style>
        /* Muda a cor do texto do label para branco */
        label {
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
        sku = st.text_input("Digite SKU para este bulto:", key=unique_key)       
        
        categorias = ["Ubicação", "Limpeza", "Tara Maior", "Costura", "Reetiquetagem"]

        # Inicializa a categoria selecionada no session_state se ainda não existir
        if "categoria_selecionada" not in st.session_state:            
            st.session_state["categoria_selecionada"] = None

        # Exibe os botões das categorias e permite a seleção
        st.markdown("<h3 style='color:white;'>Escolha uma categoria:</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)  # Criando colunas para organizar os botões

        for i, categoria in enumerate(categorias):
            btn_cor = "green" if st.session_state["categoria_selecionada"] == categoria else "gray"  # Cor do botão

            if (i % 3) == 0:
                with col1:
                    if st.button(categoria, key=f"btn_{categoria}", help=f"Selecionar {categoria}", 
                         use_container_width=True):
                        st.session_state["categoria_selecionada"] = categoria
                        st.success(f"Categoria '{categoria}' selecionada!")

            elif (i % 3) == 1:
                 with col2:
                    if st.button(categoria, key=f"btn_{categoria}", help=f"Selecionar {categoria}", 
                         use_container_width=True):
                        st.session_state["categoria_selecionada"] = categoria
                        st.success(f"Categoria '{categoria}' selecionada!")

            else:
                 with col3:
                    if st.button(categoria, key=f"btn_{categoria}", help=f"Selecionar {categoria}", 
                         use_container_width=True):
                        st.session_state["categoria_selecionada"] = categoria
                        st.success(f"Categoria '{categoria}' selecionada!")


        st_javascript("""
            setTimeout(() => {
                const inputs = document.querySelectorAll('input[type="text"]');
                if (inputs.length > 0) {
                    inputs[inputs.length - 1].focus();
                }
            }, 100);
        """)

       

        col1, col2 = st.columns(2)

        # Exibir mensagem da categoria selecionada
        if st.session_state.get("categoria_selecionada"):
            st.success(f"Categoria '{st.session_state['categoria_selecionada']}' selecionada!")

        with col1:
            if st.button("Cadastrar Peça"):
                if not st.session_state.get("bulto_numero"):
                   st.warning("Cadastre um bulto antes de cadastrar uma peça.")
                elif not st.session_state.get("categoria_selecionada"):
                   st.warning("Selecione uma categoria antes de cadastrar a peça.")
                elif not sku:
                   st.warning("Preencha o campo de SKU antes de cadastrar a peça.")
                else:
                    # Recarregar os dados do Google Sheets ANTES da verificação
                    aba = arquivo.worksheet_by_title("backstock")  # Obtém a aba correta
                    data = aba.get_all_values()
                    if data:
                          df = pd.DataFrame(data[1:], columns=data[0])  # Atualiza o DataFrame
            
                    
                    
                    
                    # Verifica se o SKU já existe na tabela antes de cadastrar
                    if "SKU" in df.columns and sku in df["SKU"].values:
                       st.error(f"SKU '{sku}' já cadastrado! Não é permitido duplicar SKUs.")
                    else:
                    # Salva os dados no Google Sheets
                       salvar_dados_no_sheets(
                           st.session_state["bulto_numero"], 
                           sku, 
                           st.session_state["categoria_selecionada"], 
                           st.session_state["user"]
                       )

                       st.success(f"Peça '{sku}' cadastrada no Bulto {st.session_state['bulto_numero']} na categoria '{st.session_state['categoria_selecionada']}'!")

                       # Resetar SKU para forçar um novo input
                       st.session_state["peca_reset_count"] = st.session_state.get("peca_reset_count", 0) + 1
                       st.rerun()



        with col2:
            if st.button("Finalizar Bulto"):
                st.success("Bulto finalizado com sucesso!")
                st.session_state["bulto_numero"] = ""
                st.session_state["bulto_cadastrado"] = False
                st.session_state["peca_reset_count"] = 0
                st.rerun()

elif selecao == "Tabela":
    #st.title("")
    st.write(df)
    
elif selecao == "Home":
    st.session_state["inicio"] = False
    st.session_state["user"] = ""  # Redefine o usuário para forçar o cadastro novamente
    st.rerun()
    
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            right: 10px;
            font-size: 12px;
            text-align: right;
            background-color: #9DD1F1;
            color: black; /* Define o texto como branco */
            padding: 5px;
            z-index: 100;
        }
    </style>
    <div class="footer">
        Copyright © 2025 Direitos Autorais Desenvolvedor Rogério Ferreira
    </div>
    """,
    unsafe_allow_html=True
)

