import os

# environment variables
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
TESSERACT = os.environ.get('TESSERACT')