import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")


# ------------------------------------
# Load Documents
# ------------------------------------
def load_documents(folder="data"):
    documents = []

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)

        # Markdown and Text Files
        if file_name.endswith(".md") or file_name.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                documents.append({
                    "source": file_name,
                    "content": f.read()
                })

        # PDF Files
        elif file_name.endswith(".pdf"):
            try:
                reader = PdfReader(file_path)

                text = ""

                for page in reader.pages:
                    extracted = page.extract_text()

                    if extracted:
                        text += extracted + "\n"

                documents.append({
                    "source": file_name,
                    "content": text
                })

            except Exception as e:
                print(f"Error reading PDF {file_name}: {e}")

    return documents


# ------------------------------------
# Chunk Documents
# ------------------------------------
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = []

    for doc in documents:

        split_chunks = splitter.split_text(
            doc["content"]
        )

        for chunk in split_chunks:

            chunks.append({
                "source": doc["source"],
                "content": chunk
            })

    return chunks


# ------------------------------------
# Create Vector Database
# ------------------------------------
def create_vector_db(chunks):

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="support_kb"
    )

    # Optional: clear old data
    try:
        existing = collection.get()
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
    except:
        pass

    for i, chunk in enumerate(chunks):

        embedding = model.encode(
            chunk["content"]
        ).tolist()

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk["content"]],
            metadatas=[
                {
                    "source": chunk["source"]
                }
            ]
        )

    return collection


# ------------------------------------
# Retrieve Relevant Chunks
# ------------------------------------
def retrieve(query, collection, top_k=3):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results