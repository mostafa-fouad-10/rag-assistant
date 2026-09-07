# Semantic Search & RAG Assistant

A lightweight document question-answering system built with **Python**, **FastAPI**, **Streamlit**, **Sentence Transformers**, **Qdrant**, and **Ollama**.

The system allows users to create projects, upload documents, process their content, and ask questions about the uploaded document using **semantic search and Retrieval-Augmented Generation (RAG)**.

---

## Features

* Create and manage projects.
* Upload documents to a specific project.
* Support for:

  * PDF
  * TXT
  * DOCX
* Persistent project and file storage.
* Document text extraction and chunking.
* Generate embeddings using **Sentence Transformers**.
* Store document vectors in **Qdrant**.
* Perform semantic similarity search.
* Retrieve relevant document chunks based on the user's question.
* Generate answers using a local **Ollama** model.
* Filter document retrieval by `file_id`.
* Interactive chat interface using **Streamlit**.
* REST API built with **FastAPI**.

---

## How It Works

The application follows a simple RAG pipeline:

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
FastAPI
 │
 ├── Project Management
 │
 ├── File Management
 │
 └── RAG Service
       │
       ├── Semantic Search
       │      │
       │      ├── Sentence Transformer
       │      └── Qdrant
       │
       └── Ollama
              │
              ▼
           Answer
```

### Document Processing

When a document is uploaded:

```text
Document
   ↓
Text Extraction
   ↓
Text Chunking
   ↓
Embedding Generation
   ↓
Vector Storage in Qdrant
```

### Question Answering

When the user asks a question:

```text
Question
   ↓
Query Embedding
   ↓
Semantic Search in Qdrant
   ↓
Retrieve Relevant Chunks
   ↓
Build Context
   ↓
Send Context + Question to Ollama
   ↓
Generate Answer
```

---

## Technologies Used

* **Python**
* **FastAPI** – Backend REST API
* **Streamlit** – Web interface
* **Sentence Transformers** – Text embeddings
* **Qdrant** – Vector database
* **Ollama** – Local LLM inference
* **Pydantic** – Data validation and configuration
* **Docker** – Running Qdrant

---

## Embedding Model

The project uses:

```text
all-MiniLM-L6-v2
```

The generated embeddings have a dimension of:

```text
384
```

Qdrant stores these vectors using **Cosine Similarity**.

---

## Local LLM

The answer generation is handled through **Ollama**.

The application communicates with Ollama using an OpenAI-compatible API.

The configured model is provided through the environment configuration.

---



## API

The backend is implemented using FastAPI.

### Projects

Create a project:

```http
POST /projects/
```

Get all projects:

```http
GET /projects/
```

Get a specific project:

```http
GET /projects/{project_id}
```

Delete a project:

```http
DELETE /projects/{project_id}
```

### Files

Upload a file:

```http
POST /files/upload/{project_id}
```

Get project files:

```http
GET /files/{project_id}
```

Delete a file:

```http
DELETE /files/delete/{project_id}/{file_id}
```

### Document Processing

The uploaded document can be processed through the document processing endpoint to extract and chunk its content.

### Semantic Search

```http
POST /search/
```

Example request:

```json
{
    "query": "What is the graduation year?",
    "limit": 5
}
```

### RAG

```http
POST /rag/
```

Example request:

```json
{
    "query": "What is the graduation year?",
    "file_id": "your-file-id"
}
```

The RAG endpoint retrieves relevant chunks from the selected document and uses them as context for generating the answer.

---

## Running the Project

### 1. Create the Conda Environment

Create and activate the project environment:

```bash
conda create -n semantic-search python=3.11
conda activate semantic-search
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
OLLAMA_BASE_URL=http://<ollama-host>:11434/v1
LOCAL_GENERATION_MODEL=llama3.2:3b
```

Make sure the selected Ollama model is available locally.

### 4. Start Qdrant

Run:

```bash
docker compose up -d
```

Qdrant will be available on:

```text
http://localhost:6333
```

### 5. Start FastAPI

From the project root:

```bash
uvicorn src.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start Streamlit

In another terminal:

```bash
streamlit run app.py
```

The Streamlit interface will open in the browser.

---

## Application Flow

1. Create a project.
2. Upload a document.
3. Process the document.
4. The document is extracted and split into chunks.
5. Chunks are converted into embeddings.
6. Embeddings are stored in Qdrant.
7. Ask a question through the chat interface.
8. The question is converted into an embedding.
9. Qdrant retrieves the most relevant chunks from the selected file.
10. The retrieved context is sent to the local Ollama model.
11. The generated answer is displayed in the Streamlit chat interface.
