from flask import Flask, json ,request
from flask_cors import CORS
import os
import pytesseract
import base64
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def get_encoded_image(image_path):
    # pil_img = Image.open(image_path, mode='r') # reads the PIL image
    # byte_arr = io.BytesIO()
    # pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    # encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    img_b64 = ""
    with open(image_path, "rb") as img:
       img_b64 = base64.b64encode(img.read())
    return img_b64.decode('utf-8')

def get_words_location(image_path):
    data = pytesseract.image_to_data(image_path, output_type='dict')
    boxes = len(data['level'])
    array_pos = []
    for i in range(boxes):
        if data['text'][i].strip() != '':
            pos = {
               "text":data['text'][i],
               "left":data['left'][i],
               "top":data['top'][i],
               "width":data['width'][i],
               "height":data['height'][i]
            }
            array_pos.append(pos)

    return array_pos

api = Flask(__name__)
CORS(api)
try:
    path = os.path.dirname(os.path.abspath(__file__))
    upload_folder=os.path.join(
    path.replace("/file_folder",""),"tmp")
    os.makedirs(upload_folder, exist_ok=True)
    api.config['upload_folder'] = upload_folder

except Exception as e:
    api.logger.info("An error occurred while creating temp folder")
    api.logger.error("Exception occurred : {}".format(e))

@api.route('/', methods=['GET'])
def index_page():
  return "API is working"

@api.route('/upload', methods=["POST"]) 
def upload_file():
  try:
    #save pdf file
    pdf_file = request.files['file']
    pdf_name = pdf_file.filename
    save_path = os.path.join(api.config.get("upload_folder"),pdf_name)
    pdf_file.save(save_path)

    images_path = os.path.join(api.config.get("upload_folder"),'working_dir')
    os.makedirs(images_path, exist_ok=True)

  
    pages = convert_from_path(save_path, poppler_path = r'C:\\poppler-23.11.0\\Library\\bin')
    
    book_words = []
    i=0
    for page in pages:
      page_img_path = os.path.join(images_path,f'{i}.png')
      page.save(page_img_path, 'PNG')
      obj = {
         "img": get_encoded_image(page_img_path),
         "words":get_words_location(page_img_path)
      }
      book_words.append(obj)
      i+=1
    
    #run tesseract to get words and its locations
    return json.dumps({ "data":book_words, "pages":i})
  except Exception as e:
    print(e)
    api.logger.info("error occurred")
    return "error"

if __name__ == '__main__':
  api.run()


