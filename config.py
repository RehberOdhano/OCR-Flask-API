import os

# environment variables
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
TESSERACT = os.environ.get('TESSERACT')