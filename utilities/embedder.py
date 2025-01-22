from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from utilities.pinecone_client import PineconeClient
import os 


INDEX_NAME = 'esgene-docx'


embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-4-turbo", api_key=os.getenv("OPENAI_API_KEY"))
pc_client = PineconeClient(api_key=os.getenv("PINECONE_API_KEY"))

# Global Embed Model
# Settings.llm = llm
# Settings.embed_model = embed_model


def create_embedding(document): 
    text_splitter = TokenTextSplitter(chunk_size=1024, chunk_overlap=100)
    text_chunks = text_splitter.split_text(document)
    
    return text_chunks
    
    
def init_vector_store(nodes): 
    index = pc_client.get_index(INDEX_NAME)
    print(f'index {index}')
