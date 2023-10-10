import streamlit as st
import replicate
import os

# Título de la aplicación
st.set_page_config(page_title="📚 EDUAI - Chatbot Educativo")

# Credenciales de Replicate
with st.sidebar:
    st.title('📚 EDUAI - Chatbot Educativo')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('¡Clave de API proporcionada!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Ingresa la clave de API de Replicate:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Por favor, ingresa tus credenciales.', icon='⚠️')
        else:
            st.success('¡Procede a ingresar tu mensaje de inicio!', icon='👉')

    st.subheader('Modelos y parámetros')
    selected_model = st.sidebar.selectbox('Elige un modelo de EDUAI', ['EDUAI-7B', 'EDUAI-13B', 'EDUAI-70B'], key='selected_model')
    if selected_model == 'EDUAI-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'EDUAI-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
    
    temperature = st.sidebar.slider('Temperatura', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('Longitud máxima', min_value=64, max_value=4096, value=512, step=8)
    
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Almacenar respuestas generadas por EDUAI
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "¿En qué puedo ayudarte hoy?"}]

# Mostrar o borrar el historial del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "¿En qué puedo ayudarte hoy?"}]
st.sidebar.button('Borrar Historial de Chat', on_click=clear_chat_history)

# Función para generar una respuesta de EDUAI
def generate_eduai_response(prompt_input):
    template = """EDUAI es un chatbot educativo diseñado para ayudarte con tus estudios de matemáticas. Siempre estoy aquí para proporcionarte información y sugerencias relacionadas con las matemáticas. Puedo ofrecerte ejercicios y material audiovisual en un formato amigable.

Estas son las áreas de matemáticas que puedo cubrir:
- Fundamentos
- Funciones
- Funciones Polinomiales y Racionales
- Funciones Exponenciales y Logarítmicas
- Funciones Trigonométricas
- Trigonometría Analítica
- Coordenadas Polares y Ecuaciones Paramétricas
- Vectores en Dos y Tres Dimensiones
- Sistemas de Ecuaciones y Desigualdades
- Secciones Cónicas

Siempre estaré disponible para ayudarte en tu proceso de aprendizaje. ¿En qué puedo ayudarte hoy?

"""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "Usuario: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "EDUAI: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{template} {prompt_input} EDUAI: ",
                                  "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1})
    return output

# Entrada proporcionada por el usuario
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generar una nueva respuesta si el último mensaje no es de EDUAI
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = generate_eduai_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
