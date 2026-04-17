import pytest
from src.preprocessing import preprocess_text
from src.model_loader import classifier
import os

def test_preprocess_text():
    raw_text = "CONFIDENTIAL: Please review Invoice #500!"
    clean_text = preprocess_text(raw_text)
    
    assert "confidential" in clean_text
    assert "please" in clean_text
    assert "review" in clean_text
    assert "invoice" in clean_text
    assert "500" not in clean_text # Removed by regex
    assert "!" not in clean_text # Removed by regex

def test_model_predict():
    # Only test if model is present, otherwise skip
    if not os.path.exists('model.pkl') or not os.path.exists('vectorizer.pkl'):
        pytest.skip("Model not trained yet.")
        
    classifier.load()
    prediction = classifier.predict("Please review the attached legal brief.")
    assert isinstance(prediction, str)
    assert len(prediction) > 0
    
def test_model_predict_empty():
    if not os.path.exists('model.pkl') or not os.path.exists('vectorizer.pkl'):
        pytest.skip("Model not trained yet.")
        
    classifier.load()
    prediction = classifier.predict("!@#")
    assert prediction == "unclassified"
