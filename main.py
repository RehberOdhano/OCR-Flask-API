from flask import Flask, json, request, jsonify
import pytesseract
from pdf2image import convert_from_bytes, convert_from_path
import os
import uuid

# environment variables
# from config import S3_BUCKET_NAME, ACCESS_KEY, SECRET_KEY
pytesseract.pytesseract.tesseract_cmd = str(os.environ.get('TESSERACT'))

# helper functions
from utils import get_encoded_image, get_words_location, allowed_file

api = Flask(__name__)

try:
  path = os.path.dirname(os.path.abspath(__file__))
  upload_folder=os.path.join(
  path.replace("/file_folder",""),"tmp")
  os.makedirs(upload_folder, exist_ok=True)
  api.config['upload_folder'] = upload_folder

except Exception as e:
  api.logger.info("An error occurred while creating temp folder")
  api.logger.error("Exception occurred : {}".format(e))

# api.config.update(
#   S3_BUCKET_NAME = S3_BUCKET_NAME,
#   ACCESS_KEY = ACCESS_KEY,
#   SECRET_KEY = SECRET_KEY
# )

# setting aws s3 client
# s3 = boto3.client(
#   's3', 
#   aws_access_key_id=api.config['ACCESS_KEY'],
#   aws_secret_access_key=api.config['SECRET_KEY']
# )

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
    
    save_path = os.path.join(api.config.get("upload_folder"), unique_file_name)
    pdf_file.save(save_path)

    images_path = os.path.join(api.config.get("upload_folder"),'working_dir')
    os.makedirs(images_path, exist_ok=True)

    pages = convert_from_path(save_path, poppler_path=str(os.environ.get('POPPLER_PATH')))
    
    # Read the content of the PDF file
    # pdf_bytes = pdf_file.read()
  
    # Convert the PDF to images
    # pages = convert_from_bytes(pdf_bytes)
    
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
    return json.dumps({ "error":e, "poppler_path": str(os.environ.get('POPPLER_PATH'))})


