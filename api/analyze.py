from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from typing import Dict, List
from utilities.csrd_graph import generate_csrd_graph

load_dotenv()

analyze_blueprint = Blueprint("analyze", __name__)
@analyze_blueprint.route("/analyze", methods=["GET"])
def analyze():
    print("Analyzing report...")
    
    csrd_graph = generate_csrd_graph()
    
    return jsonify({"status": "ok"}), 200
