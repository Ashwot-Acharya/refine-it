import chromadb
from sentence_transformers import SentenceTransformer
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_PATH = "./embeddings_store"

# Initialize ChromaDB and the SentenceTransformer model
client = None
collection = None
model = SentenceTransformer('all-MiniLM-L6-v2')      
def initialize_chromadb():
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_or_create_collection(name="reference_papers")
        if collection is None:
            raise ValueError("Failed to create or get the ChromaDB collection.")
        logging.info("ChromaDB initialized successfully.")
        return client, collection
    except Exception as e:
        logging.error(f"Error initializing ChromaDB: {e}")
        return None, None  # Return None if initialization fails

def add_reference_to_chromadb(collection, ref_file, paragraphs):
    try:
        for key, paragraph in paragraphs.items():
            embedding = model.encode(paragraph).tolist()  # Convert to list for ChromaDB compatibility
            doc_id = f"{ref_file}_{key}"
            metadata = {"file": ref_file, "key": key}
            collection.add(
                documents=[paragraph], 
                metadatas=[metadata], 
                ids=[doc_id], 
                embeddings=[embedding]
            )
        logging.info(f"Added references from {ref_file} to ChromaDB.")
    except Exception as e:
        logging.error(f"Error adding references to ChromaDB: {e}")

def query_chromadb(collection, query_text, top_n=5):
    try:
        # Encode the query text into an embedding
        query_embedding = model.encode(query_text).tolist()
        # Query ChromaDB using the embedding
        results = collection.query(query_embeddings=[query_embedding], n_results=top_n)
        return results
    except Exception as e:
        logging.error(f"Error querying ChromaDB: {e}")
        return {}