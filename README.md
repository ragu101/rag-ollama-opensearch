# RAG Pipeline with OpenSearch & Ollama (Mistral)

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline using:
- **OpenSearch** as a **vector database**
- **Ollama (Mistral)** as a **local LLM**
- **Sentence Transformer** for **text embeddings**
- **PyPDF2** for **PDF text extraction**

## 🚀 Features
- Extracts text from **PDF documents**
- **Chunks** the text for efficient search
- Converts text into **embeddings** using **SentenceTransformer**
- Stores embeddings in **OpenSearch** for fast retrieval
- Queries OpenSearch to retrieve **relevant chunks**
- Uses **Ollama (Mistral)** to generate answers based on retrieved context

## 🛠️ Architecture Diagram
```mermaid
graph TD
    subgraph User
        A[5️⃣ User Query]
    end

    subgraph RAG Pipeline
        B[1️⃣ Extract Text from PDF]
        C[2️⃣ Chunk Text]
        D[3️⃣ Generate Embeddings (Sentence Transformer)]
        E[4️⃣ Store in OpenSearch]
        F[6️⃣ Retrieve Relevant Chunks]
        G[7️⃣ Generate Response (Ollama Mistral)]
        H[8️⃣ Return Final Answer]
    end

    subgraph Data Storage
        I[(📄 PDF Documents)]
        J[(📂 OpenSearch Vector DB)]
    end

    I -->|Extract| B
    B --> C
    C -->|Generate Embeddings| D
    D -->|Store in OpenSearch| E
    E --> J

    A -->|Search Query| F
    F -->|Retrieve Context| J
    F -->|Pass Context| G
    G -->|Generate Response| H
    H -->|Return Answer| A
```

## 🏗️ Installation & Setup
### 1️⃣ Install Dependencies
```bash
pip install PyPDF2 sentence-transformers opensearch-py transformers ollama
```

### 2️⃣ Run OpenSearch in Docker
```bash
docker run -d --name opensearch -p 9200:9200 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=Tr0ub4dor2025!" opensearchproject/opensearch:latest
```

### 3️⃣ Load the Local Model in Ollama
```bash
ollama pull mistral:latest
```

## 📜 Usage
### Step 1: Ingest PDF Data
Run the Python script to extract and store document data:
```bash
python rag_setup.py
```

### Step 2: Query the System
Modify the script to ask a question:
```python
query = "What’s in my document?"
answer = generate_answer(query)
print(answer)
```

## 📌 Notes
- Ensure **OpenSearch** and **Ollama** are running before executing the script.
- The **PDF file** must be specified correctly in the script.
- Modify chunking size or model parameters for optimization.

