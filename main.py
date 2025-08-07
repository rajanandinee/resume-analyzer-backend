# main.py
# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from parser import extract_text_from_pdf
from analyzer import analyze_resume

app = FastAPI()

# (Optional) Enable CORS if frontend is added
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    resume_text = extract_text_from_pdf(contents)

    if not resume_text.strip():
        return {"message": "Text could not be extracted. Please try another file."}

    analysis = analyze_resume(resume_text)

    return {
        "message": "Resume received and analyzed.",
        "analysis": analysis
    }

# At the bottom of main.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
