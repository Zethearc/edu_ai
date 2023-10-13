import streamlit as st
from langchain import LLMChain, PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp

import gdown

# Definir el enlace de Google Drive al archivo
google_drive_url = "https://drive.google.com/file/d/1PCEFXe1WSJrFdvzUEt0Tcumzq_oPLLqS/view?usp=drive_link"

# Especificar el archivo de destino local
local_file_path = "llama-2-7b-chat.ggmlv3.q2_K.bin"

# Descargar el archivo desde Google Drive
gdown.download(google_drive_url, local_file_path, quiet=False)


TEMPLATE = """Question: {question}

Answer: """


def get_llm_chain(model_name: str) -> LLMChain:
    """Get LLMChain with LlamaCpp as LLM.

    Args:
        model_name (str): Name of the Llama model.

    Returns:
        LLMChain: LLMChain with a given model.
    """
    prompt = PromptTemplate(template=TEMPLATE, input_variables=["question"])
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCpp(
        model_path=model_name,
        callback_manager=callback_manager,
        verbose=True,
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain


def main() -> None:
    """Langchain + Streamlit + Llama = Bot 🤖"""

    st.set_page_config(page_title="Bot 🤖", layout="wide")
    st.header("Bot 🤖")
    st.markdown("Langchain 🦜️⛓️ + Streamlit 👑 + Llama 🦙")

    llm_chain = get_llm_chain(model_name=local_file_path)

    question = st.text_input("What do you want to ask?")
    button = st.button("Ask")

    if button:
        output = llm_chain.run(question)
        st.write(output)


if __name__ == "__main__":
    main()
