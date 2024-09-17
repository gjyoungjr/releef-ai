from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from utilities.embedder import create_embedding
import os 


load_dotenv()

embed_blueprint = Blueprint("embed", __name__)
@embed_blueprint.route("/embed", methods=["GET"])



def embed(): 
    document = "Our company’s latest ESG report highlights significant environmental improvements over the past year. We reduced greenhouse gas emissions by 15%, decreased water usage by 10%, and improved waste management, diverting 75% of waste from landfills. Additionally, our transition to renewable energy sources now powers 40% of our operations, contributing to a lower carbon footprint. These efforts align with our commitment to sustainability and reducing our environmental impact, ensuring responsible growth while safeguarding natural resources for future generations."

    try:
       print('Embedding report...')
       
       create_embedding(document)
       
       return jsonify({"status": "ok"}), 200
    
    except Exception as e:
        print("Error", e)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500