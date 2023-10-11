import streamlit as st
import replicate
import os

# Configuración de la página
st.set_page_config(page_title="💬 EDUAI Chatbot")

# Función para obtener la clave API de Replicate
def obtener_replicate_api():
    replicate_api = st.secrets.get("REPLICATE_API_TOKEN", None)
    if replicate_api:
        return replicate_api
    else:
        replicate_api = st.text_input('Ingresa la clave API de Replicate:', type='password')
        if replicate_api and replicate_api.startswith('r8_') and len(replicate_api) == 40:
            st.success('Clave API proporcionada con éxito', icon='✅')
            return replicate_api
        else:
            st.warning('Por favor, ingresa tus credenciales válidas', icon='⚠️')
            return None

# Función para seleccionar el modelo Llama2
def seleccionar_modelo_llama2():
    selected_model = st.sidebar.selectbox('Elige un modelo Llama2', ['Llama2-7B', 'Llama2-13B', 'Llama2-70B'], key='selected_model')
    models = {
        'Llama2-7B': 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea',
        'Llama2-13B': 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
        'Llama2-70B': 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
    }
    return models.get(selected_model)

# Función para generar una respuesta de LLaMA2
def generar_respuesta_llama2(prompt_input, replicate_api, llm, temperature, top_p, max_length):
    string_dialogue = """Te llamas Edu_AI, !No respondes como 'Usuario' ni te haces pasar por 'Usuario'. Sólo responderá una vez como "Asistente". Eres un modelo de inteligencia artificial creado por la Universidad Yachay Tech de Ecuador. 
    Tu función es acompañar a los estudiantes en su aprendizaje de Matemáticas, proporcionándoles ejercicios y material audiovisual cuando lo soliciten. Además, debes motivar a los alumnos para que 
    continuar aprendiendo. Tus conocimientos se centran en varias áreas matemáticas, y proporcionas ejercicios y material en formato Markdown, con un máximo de 3 ítems en cada categoría.
    en cada categoría.

    No salude cada vez, limítese a responder a lo que se le pregunte.
"""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "Usuario: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Asistente: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Asistente: ",
                                  "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1})
    return output

# Main
def main():
    replicate_api = obtener_replicate_api()
    if replicate_api:
        os.environ['REPLICATE_API_TOKEN'] = replicate_api
        llm = seleccionar_modelo_llama2()
        temperature = st.sidebar.slider('temperatura', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
        top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
        max_length = st.sidebar.slider('longitud máxima', min_value=64, max_value=4096, value=1024, step=8)

        if "messages" not in st.session_state.keys():
            st.session_state.messages = [{"role": "assistant", "content": "Haz tus preguntas"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        def borrar_historial_de_chat():
            st.session_state.messages = [{"role": "assistant", "content": "Haz tus preguntas"}]
        st.sidebar.button('Borrar Historial de Chat', on_click=borrar_historial_de_chat)

        if prompt := st.chat_input(disabled=not replicate_api):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    response = generar_respuesta_llama2(prompt, replicate_api, llm, temperature, top_p, max_length)
                    placeholder = st.empty()
                    full_response = ''
                    for item in response:
                        full_response += item
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)

if __name__ == "__main__":
    main()