from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
import ollama

# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text

# Step 2: Chunk text into smaller parts
def chunk_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Step 3: Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_dim = embedding_model.get_sentence_embedding_dimension()

# Step 4: Connect to OpenSearch
client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "Tr0ub4dor2025!"),
    use_ssl=True,
    verify_certs=False
)

index_name = "personal_docs"

index_body = {
    "settings": {"index": {"knn": True, "knn.algo_param.ef_search": 100}},
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "embedding": {
                "type": "knn_vector",
                "dimension": embedding_dim,
                "method": {"name": "hnsw", "space_type": "l2", "engine": "nmslib"}
            }
        }
    }
}

# Recreate index if it exists
if client.indices.exists(index_name):
    client.indices.delete(index=index_name)
client.indices.create(index=index_name, body=index_body)

# Step 5: Ingest document into OpenSearch
pdf_text = extract_text_from_pdf("Raguvaran_Madhiyan_Lead_Devops_Engineer.pdf")  # Replace with your PDF
chunks = chunk_text(pdf_text)

for i, chunk in enumerate(chunks):
    embedding = embedding_model.encode([chunk])[0].tolist()
    doc = {"text": chunk, "embedding": embedding}
    client.index(index=index_name, body=doc, id=str(i), refresh=True)

# Step 6: Query OpenSearch
def search_opensearch(query, k=3):
    query_embedding = embedding_model.encode([query])[0].tolist()
    search_body = {
        "size": k,
        "query": {"knn": {"embedding": {"vector": query_embedding, "k": k}}}
    }
    response = client.search(index=index_name, body=search_body)
    return [hit["_source"]["text"] for hit in response["hits"]["hits"]]

# Step 7: Generate answer using Ollama
def generate_answer(query):
    context_chunks = search_opensearch(query)
    context = " ".join(context_chunks)
    prompt = f"Question: {query}\nContext: {context}\nAnswer:"

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

# Step 8: Test it
query = "What’s in my document?"
answer = generate_answer(query)
print(answer)
