# Document Classification System

This is a complete, production-ready Document Classification System built with Python, FastAPI, and Scikit-Learn. It classifying text documents (e.g., invoices, reports, legal files) into predefined categories using a Machine Learning model.

## Features
- **NLP Preprocessing**: Lowercasing, stopword removal, tokenization, and character cleaning.
- **Machine Learning**: TF-IDF feature extraction and Random Forest classifier.
- **FastAPI Endpoints**: Fast and robust routing for health checking and document classification.
- **Pytest**: Automated testing of API and Model logic.

## Getting Started

### 1. Install Dependencies
Make sure you have Python 3.9+ installed.
```bash
pip install -r requirements.txt
```

### 2. Download NLTK Data
The preprocessing module requires NLTK stopwords and punkt tokenizers.
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 3. Train the Model
Run the training script. This script will generate a sample dataset, train the AI model, and save `model.pkl` and `vectorizer.pkl` in the root folder.
```bash
python train.py
```

### 4. Run the Server
Launch the FastAPI server using Uvicorn.
```bash
uvicorn src.main:app --reload
```

## Testing the API

### Health Endpoint
```bash
curl -X GET "http://127.0.0.1:8000/health"
```

### Classify Raw Text
```bash
curl -X POST "http://127.0.0.1:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Please see the attached invoice for $500 regarding recent software services."}'
```

### Classify Uploaded File
```bash
# Assuming you have a file named doc.txt
curl -X POST "http://127.0.0.1:8000/classify" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@doc.txt"
```

## Automated Tests
Run the unit tests with:
```bash
pytest
```
