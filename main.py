from fastapi import FastAPI
from api.upload import router as upload_router
from api.chat import router as chat_router
from api.document import router as document_router
app = FastAPI()

app.include_router(upload_router)


@app.get("/")
async def root():
    return {
        "message": "Rag system API is running. Use the /upload endpoint to upload PDF files."
    }
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(document_router)