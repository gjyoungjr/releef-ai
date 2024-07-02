from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os
# from utilities.pdf_helper import extract_text
# from utilities.extract_chain import extract_data

load_dotenv()

query_blueprint = Blueprint("query", __name__)
@query_blueprint.route("/query", methods=["POST"])
def ingest():
    """
    Executes a similarity search on pinecone vector store.
    """
    try:

        request_body = request.get_json()

        print(f"Request body: {request_body}")

       
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



