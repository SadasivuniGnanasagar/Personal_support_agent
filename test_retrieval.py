from src.rag_pipeline import (
    load_documents,
    chunk_documents,
    create_vector_db,
    retrieve
)

docs = load_documents()
chunks = chunk_documents(docs)

collection = create_vector_db(chunks)

query = "How can I reset my password?"

results = retrieve(query, collection)

print(results["documents"][0])