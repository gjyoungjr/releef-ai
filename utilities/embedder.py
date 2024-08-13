from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import os 

embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-4-turbo", api_key=os.getenv("OPENAI_API_KEY"))

# Global Embed Model
Settings.llm = llm
Settings.embed_model = embed_model


# TODO: Add 'typing' to func args
def create_embedding(document): 
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
    nodes = splitter.get_nodes_from_documents(document)
    print(f"Content of node 0: {nodes[1].get_content(metadata_mode='all')}")
    
    return nodes
    
 # TODO: Test function logic   
def init_vector_store(nodes): 
    vector_store = VectorStoreIndex(nodes)
   
    return vector_store