from flask import Blueprint, jsonify
from dotenv import load_dotenv
from utilities.csrd_agent import query_csrd_agent


load_dotenv()

analyze_blueprint = Blueprint("analyze", __name__)
@analyze_blueprint.route("/analyze", methods=["GET"])


def analyze():
    try:
        print("Analyzing report...")
    
        result = query_csrd_agent('Extract all guidelines that falls under the environmental aspect of the CSRD directive')
        return jsonify({"status": "ok", "text": result}), 200
       
    except Exception as e:
        print(e)
        return jsonify({"status": "error"}), 500



