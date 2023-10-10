import streamlit as st
import replicate
import os

# Título de la aplicación
st.set_page_config(page_title="🤖 Edu_AI Chatbot")

# Credenciales de Replicate
with st.sidebar:
    st.title('🤖 Edu_AI Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key ya proporcionada', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Ingresa el token de la API de Replicate:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Por favor, ingresa tus credenciales', icon='⚠️')
        else:
            st.success('Procede a ingresar tu mensaje de inicio', icon='👉')

    st.subheader('Modelos y parámetros')
    selected_model = st.sidebar.selectbox('Elige un modelo Llama2', ['Llama2-7B', 'Llama2-13B', 'Llama2-70B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
    
    temperature = st.sidebar.slider('Temperatura', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('Longitud Máxima', min_value=64, max_value=4096, value=512, step=8)
    
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Almacenar respuestas generadas por Edu_AI
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "¿En qué puedo ayudarte hoy?"}]

# Mostrar o borrar mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "¿En qué puedo ayudarte hoy?"}]
st.sidebar.button('Borrar Historial del Chat', on_click=clear_chat_history)

# Función para generar una respuesta de Edu_AI
def generate_edu_ai_response(prompt_input):
    historial_conversacion = "Eres un asistente de ayuda. No respondes como 'Usuario' ni te haces pasar por 'Usuario'. Solo respondes una vez como 'Asistente'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            historial_conversacion += "Usuario: " + dict_message["content"] + "\n\n"
        else:
            historial_conversacion += "Asistente: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{historial_conversacion}Usuario: {prompt_input} Asistente: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# Entrada de texto proporcionada por el usuario
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generar una nueva respuesta si el último mensaje no es del asistente
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = generate_edu_ai_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)