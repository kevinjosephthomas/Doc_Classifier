import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Attempt to safely ensure NLTK dependencies are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    stop_words = set(stopwords.words('english'))
except Exception:
    stop_words = set()

def preprocess_text(text: str) -> str:
    """
    Preprocess raw text:
    1. Lowercase
    2. Clean special characters
    3. Tokenize
    4. Remove stopwords
    """
    if not isinstance(text, str):
        return ""
        
    # Lowercase
    text = text.lower()
    
    # Remove special characters / digits
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Tokenize
    try:
        tokens = word_tokenize(text)
    except Exception:
        # Fallback to split if NLTK tokenizer fails
        tokens = text.split()
    
    # Remove stopwords
    if stop_words:
        tokens = [word for word in tokens if word not in stop_words]
        
    return " ".join(tokens)
