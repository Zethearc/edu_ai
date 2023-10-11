import streamlit as st
import replicate
import pinecone
import os
from sentence_transformers import SentenceTransformer, util

# Configuración de la página
st.set_page_config(page_title="💬 EDUAI Chatbot")

# Función para obtener la clave API de Replicate
def obtener_replicate_api():
    replicate_api = st.secrets.get("REPLICATE_API_TOKEN", None)
    pincone_api = st.secrets.get("PINECONE_API_TOKEN", None)
    if replicate_api and pincone_api:
        pinecone.init(api_key=pincone_api, environment="gcp-starter")
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

def generate_string_dialogue(prompt_input):
    index = pinecone.Index('edu-ai-indexes')
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    query = prompt_input
    query_vector = model.encode(query).tolist()
    ejercicios = []
    material_audiovisual = []
    responses = index.query(vector=query_vector, top_k=3, include_metadata=True)

    for respuesta in responses["matches"]:
        metadata = respuesta.get("metadata", {})
        ejercicios.append(metadata.get("Ejercicios", "No disponible"))
        material_audiovisual.append(metadata.get("Material_Audiovisual", "No disponible"))

    string_dialogue = f"""Eres un asistente para estudiantes universitarios llamado EDUAI.

    Debe seguir estrictamente las siguientes reglas a la hora de generar su respuesta.
    1. No respondas como 'Usuario' ni te hagas pasar por un 'Usuario'. Sólo responderás una vez como 'Asistente'.
    2. Cuando muestres ejercicios deben estar en formato markdown y viñetas.
    3. Si no sabes, di que no sabes y no te inventes cosas.
    4. Responde de forma concisa, directa y pertinente a la pregunta formulada.
    5. No saludes al principio de cada respuesta, limítate a contestar.

    Utiliza el siguiente material cuando te pregunten sobre un ejercicio o material audiovisual.

    {ejercicios} y {material_audiovisual}
    """
    return string_dialogue

# Función para generar una respuesta de LLaMA2
def generar_respuesta_llama2(prompt_input, replicate_api, llm, temperature, top_p, max_length):
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "Usuario: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Asistente: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{generate_string_dialogue(prompt_input)} {prompt_input} Asistente: ",
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