from flask import Flask, json, request, jsonify
import pytesseract
from pdf2image import convert_from_bytes
import os
import uuid
import boto3

# environment variables
from config import S3_BUCKET_NAME, ACCESS_KEY, SECRET_KEY
pytesseract.pytesseract.tesseract_cmd = str(os.environ.get('TESSERACT'))

# helper functions
from utils import get_encoded_image, get_words_location, allowed_file

# setting aws s3 client
s3 = boto3.client(
  's3', 
  aws_access_key_id=ACCESS_KEY,
  aws_secret_access_key=SECRET_KEY
)

api = Flask(__name__)

@api.route('/', methods=['GET'])
def index_page():
  return "API is working"

@api.route('/upload', methods=["POST"]) 
def upload_file():
  try:
    # Check if a file was included in the POST request
    if 'file' not in request.files:
      return jsonify({"error": "No file part"})
    
    # extracting the file from the request and creating a unique filename
    pdf_file = request.files['file']
    
    # Check if the file is empty
    if pdf_file.filename == '':
      return jsonify({"error": "No selected file"})
    
    # Check if the file is allowed (e.g., only accept pdf files)
    if not allowed_file(pdf_file.filename):
      return jsonify({"error": "Invalid file format"})
    
    # creating a unique name for the file
    unique_file_name = str(uuid.uuid4()) + pdf_file.filename
    
    s3_resource = boto3.resource('s3')
    s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)
    
    # uploading the file to s3 bucket
    s3_bucket.Object(unique_file_name).put(Body=pdf_file)
    
    # retrieving the saved file from s3 bucket
    pdf_file = s3.get_object(Bucket=S3_BUCKET_NAME, Key=unique_file_name)['Body']
    
    # Read the content of the PDF file
    pdf_bytes = pdf_file.read()
  
    # Convert the PDF to images
    pages = convert_from_bytes(pdf_bytes)
    
    book_words = []
    for i, image in enumerate(pages):
      obj = {
        "img": get_encoded_image(image),
        "words":get_words_location(image)
      }
      book_words.append(obj)
    print("book_words")
    print(book_words)
    return json.dumps({ "data":book_words, "pages":i})
  except Exception as e:
    print(e)
    api.logger.info("error occurred")
    return "error"


