from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
import pinecone
import transformers
import pinecone
from sentence_transformers import SentenceTransformer
import streamlit as st

embed_model_id = 'sentence-transformers/all-MiniLM-L6-v2'

pinecone.init(
    api_key=st.secrets["PINECONE_API_KEY"],
    environment=st.secrets["PINECONE_ENVIRONMENT"]
)

index_name = 'edu-ai-indexes'
index = pinecone.Index(index_name)

model_id = 'meta-llama/Llama-2-7b-chat-hf'
hf_auth = st.secrets["HF_TOKEN"]
model_config = transformers.AutoConfig.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)
model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    device_map='auto',
    use_auth_token=hf_auth
)
tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id,
    use_auth_token=hf_auth
)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
    max_length=1000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id
)

# Función para buscar en Pinecone y formatear los resultados
def buscar_en_pinecone(query):
    index = pinecone.Index('edu-ai-indexes')
    query_vector = embed_model_id.encode(query).tolist()
    ejercicios = []
    material_audiovisual = []

    responses = index.query(vector=query_vector, top_k=3, include_metadata=True)

    for respuesta in responses["matches"]:
        metadata = respuesta.get("metadata", {})
        ejercicios.append(metadata.get("Ejercicios", "No disponible"))
        material_audiovisual.append(metadata.get("Material_Audiovisual", "No disponible"))

    # Formatear los resultados como un string
    resultado_formateado = "Ejercicios:\n"
    resultado_formateado += "\n".join(ejercicios)
    resultado_formateado += "\n\nMaterial Audiovisual:\n"
    resultado_formateado += "\n".join(material_audiovisual)

    return resultado_formateado

llm = HuggingFacePipeline(pipeline=pipeline, model_kwargs={'temperature': 0.7})

prompt_template = """<s>[INST] <<SYS>>
{{Eres EDUAI, un chatbot desarrollado por Yachay Tech para ayudar a estudiantes de matemáticas. Sigue estas reglas:
    Responde como asistente.
    Sé amable, conciso y rápido.
    No saludes en cada respuesta, solo responde la pregunta.
    Anima al estudiante a seguir aprendiendo.
    Responde en español siempre.
    Utiliza el formato markdown y viñetas.
    Usa ejercicios y material audiovisual para complementar tus respuestas cuando estén disponibles.}}<<SYS>>
###

Previous Conversation:
'''
{history}
'''

{{{input}}}[/INST]

"""

memory = ConversationBufferWindowMemory(k=5)

prompt = PromptTemplate(template=prompt_template, input_variables=['input', 'history'])
chain = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

st.set_page_config(page_title="EDUAI-CHAT")

st.title("EDUAI-CHAT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = chain.run(user_prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
