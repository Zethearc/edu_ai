import streamlit as st
import replicate
import os

# Título de la aplicación
st.set_page_config(page_title="🤖 Edu_AI Chatbot")

# Creación de barra lateral
st.sidebar.title('🤖 Edu_AI Chatbot')

# Obtener la clave de la API de Replicate
replicate_api = st.sidebar.text_input('Introduce el token de la API de Replicate:', type='password')

if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
    st.sidebar.warning('Por favor, introduce tus credenciales.', icon='⚠️')
else:
    st.sidebar.success('¡Credenciales proporcionadas!', icon='✅')

# Selección del modelo Llama2
selected_model = st.sidebar.selectbox('Selecciona un modelo Llama2', ['Llama2-7B', 'Llama2-13B', 'Llama2-70B'])
models = {
    'Llama2-7B': 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea',
    'Llama2-13B': 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
    'Llama2-70B': 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
}
llm = models[selected_model]

# Parámetros de generación del chatbot
temperature = st.sidebar.slider('Temperatura', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
top_p = st.sidebar.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
max_length = st.sidebar.slider('Longitud Máxima', min_value=64, max_value=4096, value=512, step=8)

# Función para generar una respuesta de Llama2
def generate_llama2_response(prompt_input):
    conversation_history = ""
    for message in st.session_state.messages:
        if message["role"] == "user":
            conversation_history += f"Usuario: {message['content']}\n\n"
        else:
            conversation_history += f"Asistente: {message['content']}\n\n"
    response = replicate.run(llm,
                             input={"prompt": f"{conversation_history}Usuario: {prompt_input} Asistente: ",
                                    "temperature": temperature, "top_p": top_p, "max_length": max_length,
                                    "repetition_penalty": 1})
    return response

# Almacenar mensajes del chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¿En qué puedo ayudarte hoy?"}]

# Función para borrar el historial del chat
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "¿En qué puedo ayudarte hoy?"}]

# Botón para borrar el historial del chat
if st.sidebar.button('Borrar Historial del Chat', on_click=clear_chat_history):
    pass

# Entrada de texto para el usuario
prompt = st.chat_input(disabled=not replicate_api)

# Agregar mensaje del usuario al historial
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

# Generar una nueva respuesta si el último mensaje no es del asistente
if st.session_state.messages[-1]["role"] != "assistant":
    with st.spinner("Pensando..."):
        response = generate_llama2_response(prompt)
        for message in response:
            st.chat_message("assistant", message)