import json
import streamlit as st
import streamlit_authenticator as stauth
import time
from llm_api.genia import generate
from streamlit_auth.streamlit_auth import streamlit_authenticator
from utils import *

config = get_environments()
# escrevendo um título na página
st.set_page_config(page_title="Poc Chatbot", page_icon="https://cdn-icons-png.flaticon.com/512/1698/1698535.png")
cols = st.columns([65, 150])
with cols[0]:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyIQYNRPrt6QIvrg6PCK1t82JTL7G6uVwk7w&s")
with cols[1]:
    st.title("Chatbot interativo")
    st.caption("(Ver : Em desenvolvimento")
import os


authenticator = streamlit_authenticator()
try:
    authenticator.login()
except stauth.LoginError as e:
    st.error(e)

if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Bem vindo *{st.session_state["name"]}*')
    st.title('Poc Chatbot!')
             
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
    if 'kept_username' not in st.session_state:
        st.session_state['kept_username'] = st.session_state['username']

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

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                df = excel_to_dataframe(config.get('folder_xlsx'))
                responses = generate(pergunta=prompt, df=df)
                st.markdown(responses.text)
        message = {"role": "assistant", "content": responses.text}
        st.session_state.messages.append(message)