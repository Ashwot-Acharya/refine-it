import os
import json
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import summarizer as sz  # Assuming `sz` is the summarizer module you have imported.
import threading


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
        paragraphs = text.split("\n\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        for para_no, paragraph in enumerate(paragraphs, start=1):
            key = f"{page_no}_{para_no}"
            paragraph_dict[key] = paragraph
    return paragraph_dict


def summarize_pdf(text_pages):
    
    full_text = " ".join(text_pages)  # Combine all pages into one text.
    chunks = sz.split_text_into_chunks(full_text)
    summaries = [sz.summarize_text(chunk) for chunk in chunks]
    return summaries


def compute_similarity_thread(paragraph_keys, paragraphs_1, summarized_text, similarities, lock):
    """
    Threaded function to compute cosine similarity for a subset of paragraphs.
    """
    vectorizer = TfidfVectorizer()

    # Combine summarized text and subset of paragraphs for vectorization
    subset_paragraphs = [paragraphs_1[key] for key in paragraph_keys]
    all_text = subset_paragraphs + [summarized_text]
    tfidf_matrix = vectorizer.fit_transform(all_text)

    summarized_vector = tfidf_matrix[-1]  # The vector for summarized text
    for i, key in enumerate(paragraph_keys):
        para_vector = tfidf_matrix[i]
        similarity = cosine_similarity(para_vector, summarized_vector)[0][0]
        with lock:
            similarities[key] = similarity


def compute_cosine_similarity(paragraphs_1, summarized_text, num_threads=4):
    """
    Computes cosine similarity using multi-threading.
    """
    similarities = {}
    lock = threading.Lock()  # Lock to synchronize access to the `similarities` dictionary
    threads = []

    # Split paragraph keys into roughly equal chunks for each thread
    paragraph_keys = list(paragraphs_1.keys())
    chunk_size = (len(paragraph_keys) + num_threads - 1) // num_threads
    chunks = [paragraph_keys[i:i + chunk_size] for i in range(0, len(paragraph_keys), chunk_size)]

    # Create and start threads
    for chunk in chunks:
        thread = threading.Thread(
            target=compute_similarity_thread,
            args=(chunk, paragraphs_1, summarized_text, similarities, lock)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return similarities


def save_results_to_json(data, output_file):
    """
    Saves results to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Results saved to {output_file}")


def main(pdf_to_compare, reference_pdf, output_file, num_threads=4):
    """
    Main function to perform the comparison.
    """
    print("Extracting text from the first PDF...")
    text_pages_1 = extract_text_from_pdf(pdf_to_compare)
    paragraphs_1 = split_into_paragraphs(text_pages_1)

    print("Extracting and summarizing the reference PDF...")
    text_pages_2 = extract_text_from_pdf(reference_pdf)
    print(text_pages_2)
    # summarized_text = summarize_pdf(text_pages_2)

    print("Computing cosine similarity with multi-threading...")
    similarities = compute_cosine_similarity(paragraphs_1, summarized_text, num_threads=num_threads)

    print("Saving results...")
    save_results_to_json(similarities, output_file)

    print("Process completed!")


if __name__ == "__main__":
    pdf_to_compare = "./test_docs/who.pdf"  # Path to the first PDF.
    reference_pdf = "./test_docs/1503-00001.pdf"    # Path to the reference PDF.
    output_file = "./results/similarity_results.json"  # Output file path.
    num_threads = 4  # Number of threads to use.

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Run the comparison
    main(pdf_to_compare, reference_pdf, output_file, num_threads)
