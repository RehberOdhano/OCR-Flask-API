import base64
import pytesseract
import io

def allowed_file(filename):
    # Define the allowed file extensions (e.g., jpg, png, etc.)
    allowed_extensions = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_encoded_image(image):
    print("in get_encoded_image function")
    print("image")
    print(image)
    ppm_image = image.convert('RGB')

    # Save the PNG image to a byte buffer
    buffer = io.BytesIO()
    ppm_image.save(buffer, format='PNG')

    # Encode the image data in base64
    base64_encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return base64_encoded

def get_words_location(image):
    print("in get_words_location function")
    data = pytesseract.image_to_data(image, output_type='dict')
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