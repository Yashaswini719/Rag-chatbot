# RAG Chatbot

A local Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF documents and ask questions about their content. The system retrieves relevant information from the documents and uses a local LLM to generate answers.

## Features

- 📄 PDF document upload and processing
- 🔎 Hybrid search using Vector Search + BM25
- 🎯 Reranking for improved retrieval relevance
- 🧠 Conversation memory for follow-up questions
- 🤖 Local LLM using Ollama
- 🗄️ Qdrant vector database
- ⚡ FastAPI backend
- 💻 Streamlit frontend
- 📚 Source information with generated answers

## Tech Stack

**Backend:** Python, FastAPI  
**Frontend:** Streamlit  
**LLM:** Ollama (`llama3.1:8b`)  
**Embeddings:** Ollama (`nomic-embed-text`)  
**Vector Database:** Qdrant  
**Document Processing:** Docling  
**Keyword Search:** BM25  

## Architecture

```text
PDF
 ↓
Docling & Chunking
 ↓
Ollama Embeddings
 ↓
Qdrant
 ↓
Hybrid Search
(Vector + BM25)
 ↓
Reranking
 ↓
Relevant Context
 ↓
Ollama LLM
 ↓
Answer + Sources
Project Structure
Rag-app/
├── api/              # FastAPI endpoints
├── db/               # Qdrant database
├── ingestion/        # PDF processing & embeddings
├── retrival/         # Search & reranking
├── rag/              # RAG pipeline
├── llm/              # Ollama LLM
├── memory/           # Conversation history
├── Forntend/         # Streamlit UI
└── main.py           # FastAPI entry point
Run the Project

Start Qdrant:

docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

Start the FastAPI backend:

uvicorn main:app --reload

Start the Streamlit frontend:

streamlit run Forntend/app.py
Workflow

Upload a PDF → Process and chunk the document → Generate embeddings → Store in Qdrant → Search using hybrid retrieval → Rerank results → Generate an answer using the local LLM.
