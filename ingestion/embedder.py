import ollama
from uuid import uuid4

MODEL = "nomic-embed-text"


def embe_text(chunks, document_id, filename):

    emdeddings = []

    for chunk in chunks:

        response = ollama.embed(
            model=MODEL,
            input=chunk,
        )

        emdeddings.append({
            "text": chunk,
            "embedding": response.embeddings[0],
            "document_id": document_id,
            "filename": filename,
            "chunk_index": str(uuid4())
        })

    return emdeddings