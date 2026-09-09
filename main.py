from modules.pdf_loader import load_pdfs
from modules.chunker import chunks_documents
from modules.embedder import create_embeddings, create_query_embeddings
from modules.faiss_index import create_faiss_index
from modules.retriever import retrieve_chunk

documents = load_pdfs("documents")

chunks = chunks_documents(documents)

embeddings = create_embeddings(chunks)

index = create_faiss_index(embeddings)


query = "What is overfitting?"
query_embedding = create_query_embeddings(query)

results = retrieve_chunk(
    query_embedding,
    index,
    chunks,
    top_k=3
)

print("\nQuery:", query)
print("\nRetrieved Results:\n")

for result in results:
    print("Source:", result["source"])
    print("Distance:", result["distance"])
    print("Text:", result["text"][:300])
    print("-" * 60)