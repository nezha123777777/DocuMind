
def split_text(text, chunk_size=500, overlap=100):
    """
    Divise un texte en plusieurs chunks.
    """

    if chunk_size <= 0:
        raise ValueError("La taille doit être positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap invalide")

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size

        # Essayer de couper à la fin d'un mot
        if end < len(text):
            space_position = text.rfind(" ", start, end)
            if space_position > start:
                end = space_position

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def split_pages(pages, chunk_size=500, overlap=100):
    """
    Découpe les pages en chunks
    tout en conservant les numéros de page.
    """

    all_chunks = []

    for page in pages:

        text = page["text"]

        page_chunks = split_text(
            text,
            chunk_size,
            overlap
        )

        for chunk in page_chunks:
            all_chunks.append({
                "text": chunk,
                "page": page["page"]
            })

    return all_chunks
