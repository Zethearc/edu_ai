import streamlit as st
import replicate
import os

# Título de la aplicación
st.set_page_config(page_title="💬 EDUAI Chatbot")

# Credenciales de Replicate
with st.sidebar:
    st.title('💬 EDUAI Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('Clave API ya proporcionada', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Ingresa la clave API de Replicate:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Por favor, ingresa tus credenciales', icon='⚠️')
        else:
            st.success('Continúa ingresando tu mensaje de inicio', icon='👉')

    st.subheader('Modelos y parámetros')
    selected_model = st.sidebar.selectbox('Elige un modelo Llama2', ['Llama2-7B', 'Llama2-13B', 'Llama2-70B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
    
    temperature = st.sidebar.slider('temperatura', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('longitud máxima', min_value=64, max_value=4096, value=1024, step=8)
    
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Función para generar una respuesta de LLaMA2
def generar_respuesta_llama2(prompt_input):
    string_dialogue = """Eres un modelo de inteligencia artificial creado por Dario Cabezas de la Universidad Yachay Tech en Ecuador. Tu nombre es Edu_AI y respondes en español. Estás encargado de acompañar al estudiante en su proceso de aprendizaje y recomendarle ejercicios o material audiovisual sobre Matemáticas siempre que el estudiante lo solicite. Además, debes animar al estudiante a seguir estudiando y aprendiendo, y tus respuestas son siempre profesionales y amigables. 
    
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
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Asistente: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# Prompt proporcionado por el usuario
if prompt := st.text_area("Escribe tu mensaje y presiona Enter", key="user_input"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = generar_respuesta_llama2(prompt)
            full_response = ''
            for item in response:
                full_response += item
            st.write(full_response)
