from src.rag_pipeline import (
    load_documents,
    chunk_documents,
    create_vector_db
)

docs = load_documents()

chunks = chunk_documents(docs)

collection = create_vector_db(chunks)

print("Vector DB Created Successfully")
print("Chunks Stored:", len(chunks))