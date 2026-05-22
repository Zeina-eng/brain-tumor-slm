from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.summarizer import summarize_text, generate_text

app = FastAPI(title="AI Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize")
async def summarize(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    # ❌ No input
    if not text and not file:
        return {"error": "Provide text or upload a file"}

    # 🟢 If text provided
    if text:
        return {"summary": summarize_text(text)}

    # 🟢 If file uploaded
    content = await file.read()

    # TXT file
    if file.filename.endswith(".txt"):
        try:
            extracted_text = content.decode("utf-8")
        except UnicodeDecodeError:
            return {"error": "Invalid text file format. Expected utf-8 encoded text."}
        except Exception as e:
            return {"error": f"Error reading text file: {str(e)}"}
    
    # PDF file
    elif file.filename.endswith(".pdf"):
        try:
            from app.utils import extract_text_from_pdf_content
            extracted_text = extract_text_from_pdf_content(content)
        except Exception as e:
            return {"error": f"Error reading PDF: {str(e)}"}

    else:
        return {"error": "Only .txt and .pdf supported"}

    if not extracted_text.strip():
        return {"error": "File is empty"}

    summary = summarize_text(extracted_text)
    return {"summary": summary}

@app.post("/generate")
async def generate(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    # ❌ No input
    if not text and not file:
        return {"error": "Provide a prompt or upload a file"}

    # 🟢 If text provided
    if text:
        return {"generated_text": generate_text(text)}

    # 🟢 If file uploaded
    content = await file.read()
    if file.filename.endswith(".txt"):
        try:
            extracted_text = content.decode("utf-8")
        except:
            return {"error": "Invalid text file format"}
    elif file.filename.endswith(".pdf"):
        try:
            from app.utils import extract_text_from_pdf_content
            extracted_text = extract_text_from_pdf_content(content)
        except:
            return {"error": "Error reading PDF"}
    else:
        return {"error": "Only .txt and .pdf supported"}

    return {"generated_text": generate_text(extracted_text)}

# Serve the static UI files from the "static" directory
app.mount("/", StaticFiles(directory="static", html=True), name="static")