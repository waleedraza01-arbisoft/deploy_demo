from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import CrossEncoder

app = FastAPI(title="Translation Confidence Service")

# Load a small model efficient for CPU (emulating a confidence estimator)
# We use a cross-encoder which gives a score of how similar two texts are.
print("Loading model...")
model = CrossEncoder('cross-encoder/stsb-distilroberta-base')
print("Model loaded!")

class TranslationRequest(BaseModel):
    source_text: str
    translated_text: str

@app.get("/")
def health_check():
    return {"status": "active", "version": "1.0.0"}

@app.post("/predict")
def predict_confidence(request: TranslationRequest):
    try:
        # The model returns a score roughly between 0 and 1
        scores = model.predict([(request.source_text, request.translated_text)])
        confidence = float(scores[0])
        
        # Normalize simple check (just for demo purposes)
        return {
            "source": request.source_text,
            "translation": request.translated_text,
            "confidence_score": confidence,
            "quality": "High" if confidence > 0.5 else "Low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)