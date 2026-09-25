from ingestion.chunker import chunk_pdf
from ingestion.embedder import embe_text
from db.qdrant import store_embedding, create_collection


def ingest_pdf(pdf_path, document_id, filename):

    chunks = chunk_pdf(pdf_path)

    embeddings = embe_text(
        chunks,
        document_id=document_id,
        filename=filename
    )

    if embeddings:
        vector_size = len(embeddings[0]["embedding"])

        create_collection(vector_size)

        store_embedding(embeddings)

    return {
        "chunks": len(chunks),
        "vectors": len(embeddings)
    }