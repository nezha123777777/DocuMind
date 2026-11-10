
from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz
import os

app = FastAPI(
    title="DocuMind API",
    description="Assistant intelligent d'analyse documentaire",
    version="1.0.0"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Bienvenue dans DocuMind !",
        "status": "API opérationnelle"
    }


@app.post("/documents/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Veuillez importer un fichier PDF."
        )

    content = await file.read()

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Fichier PDF invalide."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(content)

    try:
        document = fitz.open(file_path)

        extracted_text = ""

        for page_number, page in enumerate(document):
            extracted_text += (
                f"\n--- Page {page_number + 1} ---\n"
                + page.get_text()
            )

        document.close()

        return {
            "filename": file.filename,
            "pages": page_number + 1,
            "extracted_text": extracted_text
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de l'extraction du PDF."
        )
