import streamlit as st
import replicate
import os

# Título de la aplicación
st.set_page_config(page_title="🦙💬 EDUAI Chatbot")

# Credenciales de Replicate
with st.sidebar:
    st.title('🦙💬 EDUAI Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('Clave de API proporcionada', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Ingresa la clave de API de Replicate:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Por favor, ingresa tus credenciales', icon='⚠️')
        else:
            st.success('Continúa ingresando tu mensaje', icon='👉')

    # Modelos y parámetros
    st.subheader('Modelos y parámetros')
    selected_model = st.sidebar.selectbox('Elige un modelo de EDUAI', ['EDUAI-7B', 'EDUAI-13B', 'EDUAI-70B'], key='selected_model')
    if selected_model == 'EDUAI-7B':
        llm = 'a16z-infra/eduai7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'EDUAI-13B':
        llm = 'a16z-infra/eduai13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/eduai70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'

    temperature = st.sidebar.slider('Temperatura', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('Longitud máxima', min_value=64, max_value=4096, value=2048, step=8)
    
    st.markdown('📖 Aprende cómo construir esta aplicación en este [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)!')
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Almacenar las respuestas generadas por EDUAI
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "asistente", "content": "¿En qué puedo ayudarte hoy?"}]

# Mostrar o borrar los mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def borrar_historial_de_chat():
    st.session_state.messages = [{"role": "asistente", "content": "¿En qué puedo ayudarte hoy?"}]
st.sidebar.button('Borrar historial de chat', on_click=borrar_historial_de_chat)

# Función para generar respuestas de EDUAI
def generar_respuesta_eduai(prompt_input):
    template = """ Eres un modelo de inteligencia artificial creado por Dario Cabezas de la Universidad Yachay Tech en Ecuador. Tu nombre es EDUAI y respondes en español. Estás encargado de acompañar al estudiante en su proceso de aprendizaje y recomendarle ejercicios o material audiovisual sobre Matemáticas siempre que el estudiante lo solicite. Además, debes animar al estudiante a seguir estudiando y aprendiendo, y tus respuestas son siempre profesionales y amigables. 
    
    Estas son tus áreas de conocimiento:

    - FUNDAMENTOS
    - FUNCIONES
    - FUNCIONES_POLINOMIALES_Y_RACIONALES
    - FUNCIONES_EXPONENCIALES_Y_LOGARITMICAS
    - FUNCIONES_TRIGONOMETRICAS_METODO_DE_LA_CIRCUNFERENCIA_UNITARIA
    - FUNCIONES_TRIGONOMETRICAS_METODO_DEL_TRIANGULO_RECTANGULO
    - TRIGONOMETRÍA_ANALÍTICA
    - COORDENADAS_POLARES_Y_ECUACIONES_PARAMÉTRICAS
    - VECTORES_EN_DOS_Y_TRES_DIMENSIONES
    - SISTEMAS_DE_ECUACIONES_Y_DESIGUALDADES
    - SECCIONES_CONICAS

    Retornas ejercicios y material audiovisual en formato agradable y Markdown con viñetas.

    """
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "usuario":
            string_dialogue += "Usuario: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Asistente: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{template} {prompt_input} Asistente: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# Prompt proporcionado por el usuario
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "usuario", "content": prompt})
    with st.chat_message("usuario"):
        st.write(prompt)

# Generar una nueva respuesta si el último mensaje no es del asistente
if st.session_state.messages[-1]["role"] != "asistente":
    with st.chat_message("asistente"):
        with st.spinner("Pensando..."):
            response = generar_respuesta_eduai(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "asistente", "content": full_response}
    st.session_state.messages.append(message)
