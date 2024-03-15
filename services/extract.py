
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from flask import Blueprint, request, jsonify


extract_blueprint = Blueprint('extract', __name__)

# Schema for the output of the data extraction
schema = {
    "properties": {
        "utility_type": {"type": "string"},
        "account_number": {"type": "string"},
        "account_name": {"type": "string"},
        "billing_date": {"type": "string"},
        "usage": {
            "type": "object",
            "properties": {
                "total_usage": {"type": "string"},
                "unit_measurement": {"type": "string"}
            }
        }
        
        
    }
}


@extract_blueprint.route('/', methods=['GET']) # TODO: Change to POST
def extract_data():
    """
    Extracts key data from a given corpus of text.
    """
            
    # llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview", api_key=api_key)
    # chain = create_extraction_chain(llm, schema)
            
    # response = chain.invoke(text)
            
    return schema
            


