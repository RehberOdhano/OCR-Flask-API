from flask import Flask, json, request, jsonify
import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
import os
import uuid
import boto3

# environment variables
from config import S3_BUCKET_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, TESSDATA_PREFIX
pytesseract.pytesseract.tesseract_cmd = str(os.environ.get('TESSERACT'))

# helper functions
from utils import get_encoded_image, get_words_location, allowed_file

# setting s3 client
# s3 = boto3.client(
#   's3', 
#   aws_access_key_id=AWS_ACCESS_KEY,
#   aws_secret_access_key=AWS_SECRET_KEY
# )

app = Flask(__name__)
# CORS(app)

@app.route('/', methods=['GET'])
def index_page():
  return "API is working"

@app.route('/upload', methods=["POST"]) 
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
    
    # print(pdf_file)
    # unique_file_name = str(uuid.uuid4()) + pdf_file.filename
    # print(unique_file_name)
    
    # s3_resource = boto3.resource('s3')
    # s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)
    
    # # uploading the file to s3 bucket
    # s3_bucket.Object(unique_file_name).put(Body=pdf_file)
    
    # # retrieving the saved file from s3 bucket
    # pdf_file = s3.get_object(Bucket=S3_BUCKET_NAME, Key=unique_file_name)['Body']
    # print(pdf_file)
    
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
    app.logger.info("error occurred")
    return "error"

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000)


