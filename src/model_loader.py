import joblib
import os
import logging
from src.preprocessing import preprocess_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self, model_path: str = 'model.pkl', vectorizer_path: str = 'vectorizer.pkl'):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None

    def load(self):
        """Loads the model and vectorizer from disk."""
        if not os.path.exists(self.model_path) or not os.path.exists(self.vectorizer_path):
            logger.warning("Model or vectorizer not found. Please run train.py first.")
            return

        try:
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            logger.info("Model and Vectorizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading models: {e}")

    def predict(self, raw_text: str) -> str:
        """Preprocesses text and predicts its class."""
        if self.model is None or self.vectorizer is None:
            raise ValueError("Model has not been initialized.")
        
        # Preprocess text
        clean_text = preprocess_text(raw_text)
        if not clean_text.strip():
            return "unclassified"
            
        # Vectorize
        features = self.vectorizer.transform([clean_text])
        
        # Predict
        prediction = self.model.predict(features)
        
        return str(prediction[0])

# Singleton instance
classifier = ModelLoader()
