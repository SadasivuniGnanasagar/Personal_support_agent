from src.rag_pipeline import load_documents, chunk_documents

docs = load_documents()

chunks = chunk_documents(docs)

print("Total Documents:", len(docs))
print("Total Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(chunks[0]["content"])