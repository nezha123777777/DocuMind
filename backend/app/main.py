
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from app.chunking import split_pages
import fitz
import uuid

app = FastAPI(
    title="DocuMind API",
    description="Assistant intelligent d'analyse documentaire",
    version="1.0.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Bienvenue dans DocuMind",
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

    file_path = UPLOAD_DIR / f"{uuid.uuid4()}.pdf"
    file_path.write_bytes(content)

    try:
        with fitz.open(file_path) as document:

            extracted_text = ""

            for page_number, page in enumerate(document):
                extracted_text += (
                    f"\n--- Page {page_number + 1} ---\n"
                    + page.get_text()
                )

            return {
                "filename": file.filename,
                "pages": len(document),
                "extracted_text": extracted_text
            }

    except Exception:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de l'extraction du PDF."
        )
