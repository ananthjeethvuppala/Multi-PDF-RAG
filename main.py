from modules.pdf_loader import load_pdfs
from modules.chunker import chunks_documents
from modules.embedder import create_embeddings, create_query_embeddings
from modules.faiss_index import create_faiss_index
from modules.retriever import retrieve_chunk
from modules.prompts import create_prompt
from modules.llm import generate_answer

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

context = ""

for result in results:
    context += f"""
Source: {result["source"]}

{result["text"]}

---------------------------------------------------------------------
"""

prompt = create_prompt(context, query)

answer = generate_answer(prompt)

print("\nQuery:", query)

print("\nRetrieved Context:\n")
print(context)

print("\nGenerated Prompt:\n")
print(prompt)

print("\nAnswer:\n")
print(answer)

print("\nSources:")

sources = set()

for result in results:
    sources.add(result["source"])

for source in sources:
    print("-", source)