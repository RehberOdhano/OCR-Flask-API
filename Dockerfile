FROM python:3.8-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install Dora
RUN pip3 install scikit-learn
RUN pip3 install pdf-info
RUN pip3 install -r requirements.txt

# Expose the port on which your application will run
EXPOSE 5000

# Define the start command for your Flask app using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:api"]