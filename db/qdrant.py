from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    PointStruct,
    VectorParams,
    Distance,
    Filter,
    FieldCondition,
    MatchValue,
)


client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION_NAME = "documents"


def create_collection(vector_size: int):

    collections = client.get_collections().collections

    exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections
    )

    if exists:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )


def store_embedding(embeddings):

    points = [
        PointStruct(
            id=str(uuid4()),
            vector=item["embedding"],
            payload={
                "text": item["text"],
                "document_id": item["document_id"],
                "filename": item["filename"],
                "chunk_index": item["chunk_index"]
            }
        )
        for item in embeddings
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


def get_documents():

    documents = {}
    offset = None

    while True:

        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False,
            offset=offset
        )

        for point in points:

            payload = point.payload or {}

            document_id = payload.get("document_id")

            if not document_id:
                continue

            if document_id not in documents:

                documents[document_id] = {
                    "document_id": document_id,
                    "filename": payload.get(
                        "filename",
                        "Unknown"
                    ),
                    "chunks": 0
                }

            documents[document_id]["chunks"] += 1

        if offset is None:
            break

    return list(documents.values())


def delete_document(document_id: str):

    try:

        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(
                            value=document_id
                        )
                    )
                ]
            )
        )

        return True

    except Exception:

        return False


def list_chunks():

    chunks = []
    offset = None

    while True:

        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=100,
            with_payload=True,
            with_vectors=False,
            offset=offset
        )

        for point in points:

            payload = point.payload or {}

            chunks.append({
                "text": payload.get("text"),
                "filename": payload.get("filename"),
                "document_id": payload.get("document_id"),
                "chunk_index": payload.get("chunk_index")
            })

        if offset is None:
            break

    return chunks