
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

ingest_blueprint = Blueprint('ingest', __name__)

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


@ingest_blueprint.route('/ingest', methods=['POST'])
def ingest():
    """
    Ingests a text document and extracts the relevant data from it
    """
    print(f'Request: {request.json}')
    
    if request.method == 'POST':
        try:
            request_data = request.json
            
            if 'text' not in request_data:
                return jsonify({'error': 'Missing "text" key in request body'}), 400
        
            text = request_data['text']
        
            # Data extraction
            llm = ChatOpenAI(temperature=0, model="gpt-4-0125-preview")
            chain = create_extraction_chain(schema, llm,)
            response = chain.invoke(text)
            
            return jsonify(response), 200
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Method not allowed'}), 405
