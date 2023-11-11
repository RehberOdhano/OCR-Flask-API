import pytesseract




# from pdf2image import convert_from_path
# import os
# path = os.path.dirname(os.path.abspath(__file__))
# upload_folder=os.path.join(path.replace("/file_folder",""),"tmp")
# pdf  = os.path.join(upload_folder,'ssp-test.pdf')
# print(pdf)
# pages = convert_from_path('kidsbook.pdf', poppler_path = r'C:\\poppler-23.11.0\\Library\\bin')
# i=0
# for page in pages:
#   page.save(f'{i}-ssp.png', 'PNG')
#   i+=1


pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
data = pytesseract.image_to_data("tmp/working_dir/3.png", output_type='dict')
boxes = len(data['level'])
print(data)

print()
print()
print()
print(boxes)
for i in range(boxes):
    if data['text'][i] != '':
        print(data['left'][i], data['top'][i], data['width'][i], data['height'][i], data['text'][i])