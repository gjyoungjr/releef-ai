from flask import Blueprint, request, jsonify
from utilities.pinecone import PineconeClient
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
import os

load_dotenv()

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
Settings.llm = llm

# TODO: Research on destructing query params for flask api 
# Allowed params - query : str, index_name : str

query_blueprint = Blueprint("query", __name__)
@query_blueprint.route("/query", methods=["GET"])
def ingest():
    """
    Executes a similarity search on pinecone vector store.
    """
    try:
        query = request.args.get('query')
        index_name = request.args.get('index_name')
        
        pc = PineconeClient()
        pc_index = pc.get_index(index_name)
        
        if not query or not index_name:
            return jsonify({"error": "Both 'query' and 'index_name' parameters are required"}), 400
        
        vector_store = PineconeVectorStore(pc_index)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        query_engine = index.as_query_engine(similarity_top_k=5, Verbose=True)
        results = query_engine.query(query)
        
        print(type(results))
        
        # Filter out built-in attributes and print remaining attributes
        # attributes = [attr for attr in dir(results) if not attr.startswith('__')]
        # print("Results attributes:", attributes)
    
        print(results.response)
  
        return jsonify({"status": "ok", "text": results.response}), 200

    except Exception as e:
        print("Error", e)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500




