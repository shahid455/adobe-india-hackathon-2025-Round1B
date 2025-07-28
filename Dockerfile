# Use Python 3.12 slim as base image
FROM --platform=linux/amd64 python:3.12-slim

# Set working directory
WORKDIR /app

# Copy entire project
COPY . .

# Install system dependencies required by PyMuPDF (fitz), etc.
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxrender1 libxext6 poppler-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy pre-downloaded SentenceTransformer model into image
COPY models /app/models

# Set entrypoint command
CMD ["python", "app/main.py"]
