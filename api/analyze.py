from flask import Blueprint, request, jsonify
from llama_index.core.node_parser import TokenTextSplitter
import os
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()


class ReportAnalyzer:
    
    def __init__(self, api_key: str, model: str = 'gpt-3.5-turbo'):
        self.api_key = api_key
        self.text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=128)
        
    # Load Guidelines 
    def load_guidelines(self) -> Dict[str, List[str]]:
        general_guidelines = [
            "Keep your ANSWER within 150 words.",
            "Be skeptical to the information disclosed in the report as there might be greenwashing.",
            "Always answer in a critical tone.",
            "Acknowledge that the information provided is representing the company's view based on its report.",
            "Scrutinize whether the report is grounded in quantifiable, concrete data or vague, unverifiable statements."
        ]
        
        tcfd_guidelines = {
            'tcfd_1': "Please concentrate on the board's direct responsibilities and actions pertaining to climate issues.",
            'tcfd_2': "Please focus on their direct duties related to climate issues.",
            'tcfd_3': "Avoid discussing the company-wide risk management system or how these risks and opportunities are identified and managed.",
            'tcfd_4': "Please do not include the process of risk identification, assessment or management in your answer.",
            'tcfd_5': "Focus solely on the resilience of strategy in these scenarios, and refrain from discussing processes of risk identification, assessment, or management strategies.",
            'tcfd_6': "Restrict your answer to the identification and assessment processes, without discussing the management or integration of these risks.",
            'tcfd_7': "Please focus on the concrete actions and strategies implemented to manage these risks, excluding the process of risk identification or assessment.",
            'tcfd_8': "Please focus on the integration aspect and avoid discussing the process of risk identification, assessment, or the specific management actions taken.",
            'tcfd_9': "Do not include information regarding the organization's general risk identification and assessment methods or their broader corporate strategy and initiatives.",
            'tcfd_10': "Confirm whether the organisation discloses its Scope 1, Scope 2, and, if appropriate, Scope 3 greenhouse gas (GHG) emissions. If so, provide any available data or specific figures on these emissions. Additionally, identify the related risks.",
            'tcfd_11': "Please detail the precise targets and avoid discussing the company's general risk identification and assessment methods or their commitment to disclosure through the TCFD."
        }

        return {"general": general_guidelines, "tcfd": tcfd_guidelines}

        
    def embed_report(self, report: str): 
        print("Embedding report...")
        chunks = self.text_splitter.split_text(report)
        print(f"Report splitted into {len(chunks)} chunks.")
        
        
analyze_blueprint = Blueprint("analyze", __name__)
@analyze_blueprint.route("/analyze", methods=["GET"])
def analyze():
    print("Analyzing report...")
    
    return jsonify({"status": "ok"}), 200
