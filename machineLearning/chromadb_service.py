import chromadb
from sentence_transformers import SentenceTransformer
import os

DB_PATH = "./embeddings_store"

# Initialize ChromaDB
def initialize_chromadb():
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name="reference_papers")
    return client, collection


# Add embeddings to ChromaDB
def add_reference_to_chromadb(collection, ref_file, paragraphs):
    model = SentenceTransformer('roberta-base')
    for key, paragraph in paragraphs.items():
        embedding = model.encode(paragraph).tolist()  # Convert to list for ChromaDB compatibility
        doc_id = f"{ref_file}_{key}"
        metadata = {"file": ref_file, "key": key}
        collection.add(documents=[paragraph], metadatas=[metadata], ids=[doc_id], embeddings=[embedding])


# Query ChromaDB for similar embeddings
def query_chromadb(collection, query_text, top_n=5):
    model = SentenceTransformer('roberta-base')
    query_embedding = model.encode(query_text).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_n)
    return results
