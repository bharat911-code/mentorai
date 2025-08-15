# Use Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); print('NLTK punkt downloaded successfully')"

# Copy application code
COPY . .

# Expose port (Render will set PORT environment variable)
EXPOSE 8000

# Make startup script executable
RUN chmod +x start.sh

# Start the application
CMD ["./start.sh"]
