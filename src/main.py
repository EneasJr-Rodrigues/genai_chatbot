import json
import streamlit as st
import streamlit_authenticator as stauth
import time
from llm_api.genia import generate
from streamlit_auth.streamlit_auth import streamlit_authenticator
from utils import *
import traceback

config = get_environments()
# escrevendo um título na página
st.set_page_config(page_title="Poc Chatbot", page_icon="https://cdn-icons-png.flaticon.com/512/1698/1698535.png")
cols = st.columns([65, 150])
with cols[0]:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyIQYNRPrt6QIvrg6PCK1t82JTL7G6uVwk7w&s")
with cols[1]:
    st.title("Chatbot interativo")
    st.caption("(Ver : Em desenvolvimento)")
import os


authenticator = streamlit_authenticator()
try:
    authenticator.login()
except stauth.LoginError as e:
    st.error(e)

if st.session_state['authentication_status']:
    stop = False
    authenticator.logout()
    st.write(f'Bem vindo *{st.session_state["name"]}*')
    st.title('Poc Chatbot!')
             
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    if 'kept_username' not in st.session_state:
        st.session_state['kept_username'] = st.session_state['username']

    uploaded_file = st.file_uploader("Faça upload de uma base para extração de indicadores:", type="xlsx")
    if stop:
        st.stop()
    if uploaded_file is not None:
        with st.spinner("Processando a base..."):
            try:
                arquivo_conteudo = uploaded_file.getvalue()
                arquivo_nome = uploaded_file.name                    
                df = excel_to_dataframe(config.get('folder_xlsx'))
                df = df.head(1000)
                st.success("Nova base carregado com sucesso!", icon="✅")
            except Exception as e:
                error_trace = traceback.format_exc()
                st.html(f"<font color='red'><b>O processo foi interrompido devido ao seguinte erro:</b></font>")
                st.error(f"Erro ao anexar a base: {error_trace}")
                stop = True                

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Como posso ajuda-lo?"}]

    # Display chat messages from history on app rerun
    for messages in st.session_state.messages:
        with st.chat_message(messages["role"]):
            st.markdown(messages["content"])  

    # React to user input
    if prompt := st.chat_input("Faça uma pergunta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

    if stop:
        st.stop()
    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                if df is not None:
                    responses = generate(pergunta=prompt, df=df)
                    st.markdown(responses.text)
                    message = {"role": "assistant", "content": responses.text}
                    st.session_state.messages.append(message)                    
                else:
                    st.error('para que eu possa responder a pergunta, anexe um arquivo')
                    stop = True