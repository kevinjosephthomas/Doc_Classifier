import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from src.preprocessing import preprocess_text
import os

def generate_sample_data():
    """Generates a dummy dataset for document classification."""
    data = {
        'text': [
            'Invoice from Supplier A for $500. Please review the attached invoice.',
            'Confidential legal contract between parties regarding non-disclosure.',
            'Monthly financial report for Q1 showing an increase in revenue.',
            'Please pay this invoice within 30 days.',
            'Legal brief for the upcoming court case v. Smith.',
            'Quarterly earnings report and balance sheet analysis.',
            'Invoice number #10293 for consulting services.',
            'The court orders a subpoena for the specified documents.',
            'Annual summary report of marketing expenditures.',
            'Overdue invoice reminder - outstanding balance $1500.'
        ],
        'label': ['invoice', 'legal', 'report', 'invoice', 'legal', 'report', 'invoice', 'legal', 'report', 'invoice']
    }
    df = pd.DataFrame(data)
    df.to_csv('sample_dataset.csv', index=False)
    print("Generated sample_dataset.csv")

def train_model():
    if not os.path.exists('sample_dataset.csv'):
        generate_sample_data()
        
    print("Loading dataset...")
    df = pd.read_csv('sample_dataset.csv')
    
    print("Preprocessing text...")
    df['clean_text'] = df['text'].apply(preprocess_text)
    
    print("Extracting features...")
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print("Saving model and vectorizer...")
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("Training complete. Artifacts saved to model.pkl and vectorizer.pkl.")

if __name__ == "__main__":
    train_model()
