import streamlit as st
from main import *
from PIL import Image
import time

img = Image.open("imagenes\logo_cs2.jpg")

st.set_page_config(page_title="Chatbot CS2", page_icon=img)

st.markdown(
    """
    <style>
    
    /* Change font size and color for h1 */
    h1 {
        font-family: 'Helvetica';
        font-style: italic;
        font-size: 50px;
        text-align: center;
    }
    
    /* Change font size for all markdown text */
    .markdown-text {
        font-size: 23px;
    }

    .stApp {
        background-image: url('https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwallpapercave.com%2Fwp%2Fwp2923112.jpg&f=1&nofb=1&ipt=2929843096527e5526fdeb215d1c1ff4e7f532ff93706efbfc575f1c42fc03f9&ipo=images');
        background-size: cover; /* Ajustar imagen al tamaño de la pantalla */
    }
    .css-1d391kg, .css-16idsys, .css-10trblm, .css-16huue1 {
        background-color: #ffffff; /* Blanco para los contenedores */
        border-radius: 5px; /* Bordes redondeados */
        padding: 10px; /* Espaciado interno */
    }
    </style>
    """,
    unsafe_allow_html=True
)

usuario = "🫡"
bot = "🪖"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
h1 = st.title("Bienvenido soldado.")

    
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = usuario if message['role'] == "user" else bot
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        
# Accept user input
if prompt := st.chat_input("Escriba su consulta aqui"):
    while prompt is None:
        time.sleep()
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=usuario):
        st.markdown(prompt)
        
        chat_history = "\n".join([message["content"] for message in st.session_state.messages if message["role"] == "user"])

    with st.chat_message("assistant", avatar=bot):
        contenedor_mensaje = st.empty()
        full_response= ""
        
        assistant_response = chatbot(prompt, chat_history)
        for chunk in assistant_response.split():
            full_response += chunk + ' '
            time.sleep(0.10)
            contenedor_mensaje.markdown(full_response + "▌")
        
        #st.markdown(assistant_response)
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Uncomment if you want to hide Streamlit style elements
hide_st_style = """
             <style>
             #MainMenu {visibility: hidden;}
             footer {visibility: hidden;}
             header {visibility: hidden;}
             </style>
             """
st.markdown(hide_st_style, unsafe_allow_html=True)