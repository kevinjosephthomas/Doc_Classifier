from fastapi import APIRouter, HTTPException, File, UploadFile, Request
from src.model_loader import classifier

router = APIRouter()

@router.post("/classify", tags=["Classification"])
async def classify_document(request: Request):
    """
    Classifies a document based on JSON payload {"text": "..."} or an uploaded text file.
    """
    raw_text = None
    content_type = request.headers.get("Content-Type", "")
    
    if "application/json" in content_type:
        try:
            body = await request.json()
            raw_text = body.get("text")
        except Exception:
            pass
    elif "multipart/form-data" in content_type:
        try:
            form = await request.form()
            if "file" in form:
                file_field = form["file"]
                # file_field is an UploadFile like object
                content = await file_field.read()
                raw_text = content.decode("utf-8", errors="ignore")
            elif "text" in form:
                raw_text = form["text"]
        except Exception:
            pass

    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=400, detail="No text provided. Please provide JSON text or a text file.")
        
    try:
        category = classifier.predict(raw_text)
        return {
            "status": "success",
            "category": category
        }
    except ValueError as e:
        raise HTTPException(status_code=503, detail="Model is not loaded properly. Have you trained it?")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
