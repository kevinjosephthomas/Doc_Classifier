# Use official lean python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if required for PyPDF2 or multipart
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the backend code
COPY . .

# Expose port 8000
EXPOSE 8000

# Start FastAPI exactly like the user's running terminal
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
