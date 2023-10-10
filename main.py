import streamlit as st
import replicate
import os

# Configuración de la página de la aplicación
st.set_page_config(page_title="📚 EDUAI Chatbot")

# Credenciales de Replicate
with st.sidebar:
    st.title('📚 EDUAI Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('Clave de API ya proporcionada', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Introduce la clave de la API de Replicate:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('¡Por favor, introduce tus credenciales!', icon='⚠️')
        else:
            st.success('Procede a ingresar tu mensaje de solicitud.', icon='👉')

    # Modelos y parámetros
    st.subheader('Modelos y parámetros')
    selected_model = st.sidebar.selectbox('Elige un modelo de Llama2', ['Llama2-7B', 'Llama2-13B', 'Llama2-70B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e'
    elif selected_model == 'Llama2-13B':
        llm = 'meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d'
    else:
        llm = 'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3'
    
    temperature = st.sidebar.slider('temperatura', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('longitud máxima', min_value=64, max_value=4096, value=2048, step=8)
    
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Almacenamiento de respuestas generadas por LLM
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "¿En qué puedo ayudarte hoy?"}]

# Mostrar o borrar mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "¿En qué puedo ayudarte hoy?"}]
st.sidebar.button('Borrar Historial del Chat', on_click=clear_chat_history)

# Función para generar una respuesta de Llama2
def generate_llama2_response(prompt_input):
    string_dialogue = """EDUAI es un chatbot educativo diseñado para ayudarte con tus estudios de matemáticas. Siempre estoy aquí para proporcionarte información y sugerencias relacionadas con las matemáticas. Puedo ofrecerte ejercicios y material audiovisual en un formato amigable. Estas son las áreas de matemáticas que puedo cubrir: - Fundamentos - Funciones - Funciones Polinomiales y Racionales - Funciones Exponenciales y Logarítmicas - Funciones Trigonométricas - Trigonometría Analítica - Coordenadas Polares y Ecuaciones Paramétricas - Vectores en Dos y Tres Dimensiones - Sistemas de Ecuaciones y Desigualdades - Secciones Cónicas Siempre estaré disponible para ayudarte en tu proceso de aprendizaje. ¿En qué puedo ayudarte hoy? No respondas como 'Usuario' o finjas ser 'Usuario'. Solo responde una vez como 'Asistente'."""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "Usuario: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Asistente: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Asistente: ",
                                  "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1})
    return output

# Solicitud proporcionada por el usuario
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generar una nueva respuesta si el último mensaje no es del asistente
if st.session_state.messages[-1]["role"] != "asistente":
    with st.chat_message("asistente"):
        with st.spinner("Pensando..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "asistente", "content": full_response}
    st.session_state.messages.append(message)
