from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from typing import Dict, List
from utilities.csrd_graph import generate_csrd_graph
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain import OpenAI, LLMChain
from langchain.tools import DuckDuckGoSearchRun
from langchain.vectorstores import FAISS

from typing import List, Union
from langchain.schema import AgentAction, AgentFinish
import re
import langchain
load_dotenv()

analyze_blueprint = Blueprint("analyze", __name__)
@analyze_blueprint.route("/analyze", methods=["GET"])


def analyze():
    print("Analyzing report...")
    
    csrd_graph = generate_csrd_graph()
    
    text = []
    metadata = []

    for node_id, node_data in csrd_graph.nodes(data=True):
        text.append(node_data['title'])
        metadata.append({'id': node_id, 'label': node_data['label']})
    
    embeddings = OpenAIEmbeddings()
    csrd_vector_store = FAISS.from_texts(text, embeddings, metadatas=metadata)
    
    return jsonify({"status": "ok"}), 200
