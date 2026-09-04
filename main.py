from modules.pdf_loader import load_pdfs

documents = load_pdfs("documents")
print("Total Documents:",len(documents))

for document in documents:
    print("\nSource", document["source"])
    print("Characters",len(document["text"]))