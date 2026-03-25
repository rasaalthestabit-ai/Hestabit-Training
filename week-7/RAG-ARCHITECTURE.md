# RAG Architecture (Retrieval-Augmented Generation)

## Overview

This project implements a **modular, production-ready Retrieval-Augmented Generation (RAG) pipeline** that supports:

* 📄 Multi-format data ingestion (PDF, CSV, DOCX, Images)
* 🧹 Text cleaning and preprocessing
* ✂️ Intelligent chunking
* 🧠 Semantic embeddings
* 🔎 Vector similarity search using FAISS
* 💬 Query-based retrieval system

---

## 🏗️ High-Level Architecture

```
                ┌──────────────────────┐
                │   Raw Data Sources   │
                │ (PDF, CSV, DOCX, IMG)│
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │     Loaders          │
                │ (parse documents)    │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │    Text Cleaner      │
                │ (normalize text)     │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │     Chunking         │
                │ (split into pieces)  │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │   Metadata Builder   │
                │ (source tracking)    │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │     Embeddings       │
                │ (vector conversion)  │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │     FAISS Store      │
                │ (vector database)    │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │     Query Engine     │
                │ (semantic search)    │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │   Retrieved Context  │
                └──────────────────────┘
```

---

## 🔄 Data Flow Explained

### 1. Data Ingestion

Raw files are stored in:

```
src/data/raw/
```

Supported formats:

* PDF
* CSV
* DOCX
* Images (PNG, JPG, JPEG)

Each file is processed using **custom loaders**.

---

### 2. Text Cleaning

The cleaning module:

* Removes extra whitespace
* Normalizes line breaks
* Prepares text for chunking

```python
clean_text(text)
```

---

### 3. Chunking

Text is split into overlapping chunks:

* Improves retrieval accuracy
* Maintains context continuity

```python
chunk_text(text)
```

---

### 4. Metadata Creation

Each chunk is enriched with metadata:

```json
{
  "source": "file_name",
  "chunk_id": 3,
  "text": "actual chunk text"
}
```

This enables:

* Traceability
* Better retrieval
* Source attribution

---

### 5. Embedding Generation

Chunks are converted into vectors using:

```python
Embedder().embed(chunks)
```

These vectors represent semantic meaning.

---

### 6. Vector Storage (FAISS)

Embeddings are stored in FAISS:

* Fast similarity search
* Scalable retrieval
* Local vector database

```python
FAISSStore.add(vectors, metadata)
```

---

### 7. Query Processing

User query flow:

```
User Query → Embedding → Vector Search → Top-K Results
```

```python
engine.query("your question")
```

---

### 8. Retrieval Output

Returns:

* Most relevant chunks
* Associated metadata
* Source context

---

## 📁 Project Structure

```
src/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── chunks/
├── pipelines/
│   └── ingest.py
├── utils/
│   ├── loaders.py
│   ├── cleaner.py
│   ├── chunker.py
│   └── metadata.py
├── embeddings/
│   └── embedder.py
├── vectorstore/
│   └── faiss_store.py
├── query_engine.py
└── config/
    └── settings.py
```

---

## ⚙️ Key Design Decisions

### ✅ Modular Architecture

Each component is independent and replaceable.

---

### ✅ Separation of Concerns

| Component    | Responsibility      |
| ------------ | ------------------- |
| Loaders      | Data parsing        |
| Cleaner      | Text normalization  |
| Chunker      | Text splitting      |
| Embedder     | Vector generation   |
| Vector Store | Storage & retrieval |

---

### ✅ Metadata + Text Together

Critical design:

```python
{
  **metadata,
  "text": chunk
}
```

👉 Ensures retrieved results contain actual content

---

### ✅ Offline Capability

* No dependency on external APIs
* Works locally with FAISS

---

## 🚀 Future Improvements

* 🔹 Add LLM for answer generation
* 🔹 Hybrid search (keyword + semantic)
* 🔹 Reranking models
* 🔹 Multimodal embeddings (image + text)
* 🔹 Streaming responses
* 🔹 API deployment (FastAPI)

---

## 🧪 How to Run

### Step 1: Ingest Data

```bash
python src/pipelines/ingest.py
```

---

### Step 2: Query System

```bash
python src/query_engine.py
```

---

## 🧠 Summary

This RAG system enables:

* Efficient document understanding
* Scalable semantic search
* Foundation for AI assistants

---

## 💡 Key Insight

> RAG = Retrieval + Context + Generation

Currently implemented:

✔ Retrieval
✔ Context

Next step:

➡️ Generation (LLM integration)

---

## 📌 Author

Built as part of an advanced **GenAI + RAG pipeline training project**.
