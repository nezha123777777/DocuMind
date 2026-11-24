
from app.chunking import split_pages

pages = [
    {
        "page": 1,
        "text": """
        DocuMind est une plateforme intelligente
        basée sur l'intelligence artificielle.
        Elle permet d'analyser des documents PDF.
        """
    },
    {
        "page": 2,
        "text": """
        Le système utilise le RAG.
        Il recherche les passages pertinents
        avant de générer une réponse.
        """
    }
]

chunks = split_pages(
    pages,
    chunk_size=100,
    overlap=20
)

for i, chunk in enumerate(chunks):

    print(f"\nCHUNK {i + 1}")
    print("Page :", chunk["page"])
    print("Texte :", chunk["text"])
