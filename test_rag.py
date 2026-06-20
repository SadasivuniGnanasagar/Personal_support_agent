from src.rag_pipeline import load_documents

docs = load_documents()

print(f"Total Documents Loaded: {len(docs)}")

for doc in docs:
    print("\n------------------")
    print("Source:", doc["source"])
    print("Preview:", doc["content"][:100])