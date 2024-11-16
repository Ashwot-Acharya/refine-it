import os
import json
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import summarizer as sz  # Assuming `sz` is the summarizer module you have imported.
import threading
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor, as_completed
from sentence_transformers import SentenceTransformer, util
from chromadb_service import initialize_chromadb, query_chromadb, add_reference_to_chromadb


SIMILARITY_THRESHOLD = 0.7


def save_results_to_json(data, output_file):
    """
    Saves results to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Results saved to {output_file}")


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file and organizes it into paragraphs by pages.
    """
    try:
        reader = PdfReader(pdf_path)
        text_pages = [page.extract_text() for page in reader.pages]
        return text_pages
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return []


def split_into_paragraphs(text_pages):
    """
    Splits the text from pages into paragraphs.
    """
    paragraph_dict = {}
    for page_no, text in enumerate(text_pages, start=1):
        paragraphs = text.split("\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        for para_no, paragraph in enumerate(paragraphs, start=1):
            key = f"{page_no}_{para_no}"
            paragraph_dict[key] = paragraph
    return paragraph_dict
    
def summarizing_using_gemini(text): 
    genai.configure(api_key="AIzaSyCpUhPjTcd9SudXgO2SAHtdoaUC3z4uKoU")
    model = genai.GenerativeModel("gemini-1.5-flash-8b ")
    response = model.generate_content(f"give me the gist of {text}")
    print(response.text)
    return response.text 

def summarize_pdf(text_pages):
    
    full_text = " ".join(text_pages)  # Combine all pages into one text.
    chunks = sz.split_text_into_chunks(full_text)
    summaries = [sz.summarize_text(chunk) for chunk in chunks]
    return summaries


def compute_cosine_similarity(paragraphs_1, comparing_text, num_threads=4):
    similarity_results = {}
    model = SentenceTransformer('roberta-base')

    # Function to summarize a paragraph
    def summarize_paragraph(key, paragraph):
        summarized = sz.summarize_text(paragraph)  # Summarize the paragraph
        return key, summarized

    # Use multithreading for summarization
    summarized_paragraphs = {}
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_key = {executor.submit(summarize_paragraph, key, paragraph): key for key, paragraph in paragraphs_1.items()}

        # Collect results as they complete
        for future in as_completed(future_to_key):
            key, summarized = future.result()
            summarized_paragraphs[key] = summarized

    # Compute cosine similarity sequentially after summarization
    for key, summarized_paragraph in summarized_paragraphs.items():
        texts = [summarized_paragraph, comparing_text]
        embeddings = model.encode(texts, convert_to_tensor=True)

        similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)
        similarity_value = similarity_matrix[0, 1].item()

        similarity_results[key] = similarity_value

        # Save intermediate results
        save_results_to_json(similarity_results, "similarity.json")

    # Print final results
    for key, similarity in similarity_results.items():
        print(f"Similarity for {key}: {similarity}")

    return similarity_results    


def process_uploaded_pdf(uploaded_file_path, reference_folder, num_threads=4):
    """
    Processes the uploaded PDF and compares it with reference PDFs stored in ChromaDB.
    """
    client, collection = initialize_chromadb()
    text_pages_1 = extract_text_from_pdf(uploaded_file_path)
    paragraphs_1 = split_into_paragraphs(text_pages_1)

    # Load and summarize the uploaded document
    uploaded_full_text = " ".join(text_pages_1)
    uploaded_summary = summarizing_using_gemini(uploaded_full_text)

    # Query ChromaDB for similarities
    similarities = {}
    results = query_chromadb(collection, uploaded_summary, top_n=5)

    for i, result in enumerate(results["metadatas"]):
        ref_file = result["file"]
        ref_key = result["key"]
        similarity_score = results["distances"][i]  # Lower distance means higher similarity
        if similarity_score <= 0.3:  # Adjust threshold for your application
            similarities[ref_file] = similarities.get(ref_file, [])
            similarities[ref_file].append({"paragraph_key": ref_key, "similarity_score": 1 - similarity_score})

    return similarities

def main(pdf_to_compare, reference_pdf, output_file, num_threads=4):
    """
    Main function to perform the comparison.
    """
    print("Extracting text from the first PDF...")
    text_pages_1 = extract_text_from_pdf(pdf_to_compare)
    paragraphs_1 = split_into_paragraphs(text_pages_1)


    print("Extracting and summarizing the reference PDF...")
    text_pages_2 = extract_text_from_pdf(reference_pdf)
    summarized_text =  summarizing_using_gemini(text_pages_2)

    
    # summarized_text = summarize_pdf(text_pages_2)

    print("Computing cosine similarity with multi-threading...")
    similarities = compute_cosine_similarity(paragraphs_1, summarized_text, num_threads=num_threads)

    print("Saving results...")
    save_results_to_json(similarities, output_file)

    print("Process completed!")


if __name__ == "__main__":
    pdf_to_compare = "./test_docs/who.pdf"  # Path to the first PDF.
    reference_pdf = "./test_docs/1504-00001.pdf"    # Path to the reference PDF.
    output_file = "./results/similarity_results.json"  # Out    put file path.
    num_threads = 4  # Number of threads to use.

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Run the comparison
    main(pdf_to_compare, reference_pdf, output_file, num_threads)
