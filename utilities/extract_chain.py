from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
import json 

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
                "unit_measurement": {"type": "string"},
            },
        },
    }
}

def extract_data(text: str) -> dict:
    """
    Extracts data from the text using the extraction chain
    """
    
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview")
    chain = create_extraction_chain(schema, llm)
    
    response = chain.invoke(text)
    print(json.dumps(response, indent=2))
    
    return response['text']