from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import boto3
import os
from utilities.pdf_helper import extract_text
from utilities.extract_chain import extract_data

load_dotenv()


s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["AWS_REGION"],
)

extract_blueprint = Blueprint("extract", __name__)
@extract_blueprint.route("/extract", methods=["POST"])
def ingest():
    """
    Ingests a text document and extracts the relevant data from it
    """
    try:

        request_body = request.get_json()

        key = request_body["file_key"]
        bucket = request_body["bucket"]

        # Get the file from S3
        s3_response = s3_client.get_object(Bucket=bucket, Key=key)
        
        file_stream = s3_response["Body"].read() 
        file_type = s3_response["ContentType"].split('/')[1]
        
        text = extract_text(file_stream, file_type)
        data = extract_data(text)

       
        return jsonify({"status": "ok", "data": data}), 200

    except Exception as e:
        # Handle any exceptions
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



