from fastapi import APIRouter, HTTPException

from db.qdrant import get_documents, delete_document


router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


@router.get("")
def documents():
    return {
        "documents": get_documents()
    }


@router.delete("/{document_id}")
def remove_document(document_id: str):
    deleted = delete_document(document_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "message": "Document deleted successfully.",
        "document_id": document_id
    }