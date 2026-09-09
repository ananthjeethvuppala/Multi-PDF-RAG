from modules.pdf_loader import load_pdfs
from modules.chunker import chunks_documents
from modules.embedder import create_embeddings, create_query_embeddings
from modules.faiss_index import create_faiss_index

documents = load_pdfs("documents")

chunks = chunks_documents(documents)

embeddings = create_embeddings(chunks)

index = create_faiss_index(embeddings)

print("Total Documents:",len(documents))
print("Total chunks:", len(chunks))

print("\nFirst 5 Chunks:\n")

for chunk_index, chunk in enumerate(chunks[:5]):
    print(f"Chunk {chunk_index + 1}")
    print(f"Source: {chunk['source']}")
    print(chunk["text"])
    print("-" * 60)

print("Embeddings Shape:", embeddings.shape)
print("FAISS Index Size:", index.ntotal)