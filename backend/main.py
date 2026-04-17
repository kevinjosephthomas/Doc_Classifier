import os
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
import PyPDF2

# Load env variables from .env file in the same directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI(title="Document Classifier API")

# Allow React dev server to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:30080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = (
    "You are a highly intelligent document classification assistant. "
    "Read the provided document text and identify what category of document it is "
    "(e.g., Invoice, Legal Contract, Financial Report, Medical Record, Resume, Research Paper, etc.). "
    "Respond EXCLUSIVELY in valid JSON format with the following keys:\n"
    "- \"type\": string (The Category)\n"
    "- \"confidence\": integer (A confidence score between 0 and 100)\n"
    "- \"reason\": string (One concise sentence explaining your classification)\n"
    "- \"word_count\": integer (An estimation of the document length)\n"
    "Do not include any markdown formatting like ```json or any other text before/after the JSON."
)

def extract_text(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    else:
        return file_bytes.decode("utf-8", errors="ignore")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not set. Please add it to backend/.env."
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        document_text = extract_text(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text: {e}")

    if not document_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from the file.")

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Document Text:\n\n{document_text[:6000]}"}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.1,
            max_tokens=300,
            response_format={"type": "json_object"}
        )
        result_str = response.choices[0].message.content
        import json
        result_data = json.loads(result_str)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Groq API error: {e}")

    return {
        "filename": file.filename,
        "result": result_data,
        "preview": document_text[:500],
    }
