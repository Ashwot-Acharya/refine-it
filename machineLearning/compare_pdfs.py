import os
import json
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import summarizer as sz  # Assuming `sz` is the summarizer module you have imported.

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
    """
    Summarizes the extracted text of a PDF using the summarizer module `sz`.
    """
    full_text = " ".join(text_pages)  # Combine all pages into one text.
    summary = sz.summarize_text(full_text)  # Summarize using `sz`.
    return summary

def compute_cosine_similarity(paragraphs_1, summarized_text):
    """
    Computes cosine similarity between paragraphs of the first file and the summarized text.
    """
    vectorizer = TfidfVectorizer()
    similarities = {}

    # Combine summarized text and paragraphs for vectorization
    all_text = list(paragraphs_1.values()) + [summarized_text]
    tfidf_matrix = vectorizer.fit_transform(all_text)

    summarized_vector = tfidf_matrix[-1]  # The vector for summarized text
    for key, paragraph in paragraphs_1.items():
        para_vector = tfidf_matrix[all_text.index(paragraph)]
        similarity = cosine_similarity(para_vector, summarized_vector)
        similarities[key] = similarity[0][0]

    return similarities

def save_results_to_json(data, output_file):
    """
    Saves results to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Results saved to {output_file}")

def main(pdf_to_compare, reference_pdf, output_file):
    """
    Main function to perform the comparison.
    """
    print("Extracting text from the first PDF...")
    text_pages_1 = extract_text_from_pdf(pdf_to_compare)
    paragraphs_1 = split_into_paragraphs(text_pages_1)

    print("Extracting and summarizing the reference PDF...")
    text_pages_2 = extract_text_from_pdf(reference_pdf)
    summarized_text = summarize_pdf(text_pages_2)

    print("Computing cosine similarity...")
    similarities = compute_cosine_similarity(paragraphs_1, summarized_text)

    print("Saving results...")
    save_results_to_json(similarities, output_file)

    print("Process completed!")


# if __name__ == "__main__":
#     # Example usage:
#     pdf_to_compare = "./pdfs/document_1.pdf"  # Path to the first PDF.
#     reference_pdf = "./pdfs/reference.pdf"    # Path to the reference PDF.
#     output_file = "./results/similarity_results.json"  # Output file path.

#     # Ensure output directory exists
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)

#     # Run the comparison
#     main(pdf_to_compare, reference_pdf, output_file)
