import chromadb
from chromadb.utils import embedding_functions
import pandas as pd

# Cargar el DataFrame desde el archivo CSV
df = pd.read_csv("datos_embeddings.csv")

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')
chroma_client = chromadb.Client()
client_persistent = chromadb.PersistentClient(path='data_embeddings')
client_persistent.delete_collection(name="edu_ai")
db = client_persistent.create_collection(name='edu_ai', embedding_function=sentence_transformer_ef)

db.add(
    ids = df['ids'].astype(str).tolist(),
    documents=df['text'].tolist(),
    metadatas= df.drop(['ids','embeddings','text'],axis=1).to_dict('records')
)