from sentence_transformers import SentenceTransformer
import logging
from chromadb_service import initialize_chromadb

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-mpnet-base-v2')  # Ensure this model matches your collection's embedding dimension

def search_similar_papers(query_text, top_n=5):
    """
    Searches ChromaDB for papers with high similarity to the query text.
    
    Args:
        query_text (str): The text to search for similar papers.
        top_n (int): The number of top similar papers to retrieve.
    
    Returns:
        list: A list of dictionaries containing information about similar papers.
    """
    try:
        # Initialize ChromaDB client and collection
        client, collection = initialize_chromadb()
        if client is None or collection is None:
            raise ValueError("Failed to initialize ChromaDB. Check the database configuration.")
        
        # Encode the query text into an embedding
        query_embedding = model.encode(query_text).tolist()
        
        # Query ChromaDB for similar papers
        results = collection.query(query_embeddings=[query_embedding], n_results=top_n)
        
        # Process and return the results
        similar_papers = []
        for i, metadata_entry in enumerate(results.get("metadatas", [])[0]):
            similarity_score = 1 - results.get("distances", [[1.0] * len(results.get("metadatas", []))])[0][i]
            paper_info = {
                "reference_file": metadata_entry.get("file"),
                "paragraph_key": metadata_entry.get("key"),
                "similarity_score": similarity_score,
            }
            similar_papers.append(paper_info)
        
        return similar_papers
    
    except Exception as e:
        logging.error(f"Error searching for similar papers: {e}")
        return []

# Example usage
query_text = "This is an example query to find similar research papers."
top_similar_papers = search_similar_papers(query_text, top_n=5)
print(top_similar_papers)