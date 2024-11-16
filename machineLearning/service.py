import os
import json
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from chromadb_service import initialize_chromadb, add_reference_to_chromadb, query_chromadb
import summarizer as sz  # Assuming this is your custom summarizer module
import google.generativeai as genai
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SIMILARITY_THRESHOLD = 0.7
TIMEOUT_SECONDS = 30  # Timeout for long-running operations

def save_results_to_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    logging.info(f"Results saved to {output_file}")

def load_metadata(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error loading metadata from {json_file}: {e}")
        return {}

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text_pages = [page.extract_text() for page in reader.pages]
        logging.info(f"Extracted text from {pdf_path}")
        return text_pages
    except Exception as e:
        logging.error(f"Error reading PDF {pdf_path}: {e}")
        return []

def split_into_paragraphs(text_pages):
    paragraph_dict = {}
    for page_no, text in enumerate(text_pages, start=1):
        if not text:
            continue
        paragraphs = text.split("\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        for para_no, paragraph in enumerate(paragraphs, start=1):
            key = f"{page_no}_{para_no}"
            paragraph_dict[key] = paragraph
    return paragraph_dict

def summarizing_using_gemini(text):
    try:
        genai.configure(api_key="YOUR_API_KEY_HERE")
        model = genai.GenerativeModel("gemini-1.5-flash-8b")
        response = model.generate_content(f"give me the gist of: {text}")
        return response.text
    except Exception as e:
        logging.error(f"Error summarizing text with Gemini: {e}")
        return ""

def format_mla_citation_from_metadata(key, metadata):
    details = metadata.get(key, [])
    author = "Unknown Author"
    title = "Unknown Title"
    file = key

    for line in details:
        if line.startswith("Authors:"):
            author = line.replace("Authors:", "").strip()
        elif line.startswith("Title:"):
            title = line.replace("Title:", "").strip()

    return f"{author}. \"{title}.\" {file}, accessed via the comparison system."

def save_citations_to_file(citations, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Citations in MLA Format\n")
        file.write("========================\n\n")
        for citation in citations:
            file.write(f"{citation}\n\n")
    logging.info(f"Citations saved to {output_file}")

def compute_cosine_similarity(paragraphs_1, comparing_text, model, num_threads=4):
    similarity_results = {}

    def summarize_and_embed(key, paragraph):
        try:
            summarized = sz.summarize_text(paragraph)
            texts = [summarized, comparing_text]
            embeddings = model.encode(texts, convert_to_tensor=True)
            similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)
            similarity_value = similarity_matrix[0, 1].item()
            return key, similarity_value
        except Exception as e:
            logging.error(f"Error processing paragraph {key}: {e}")
            return key, None

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_key = {executor.submit(summarize_and_embed, key, paragraph): key for key, paragraph in paragraphs_1.items()}

        for future in as_completed(future_to_key):
            try:
                key, similarity_value = future.result(timeout=TIMEOUT_SECONDS)
                if similarity_value is not None:
                    similarity_results[key] = similarity_value
            except TimeoutError:
                logging.warning(f"Processing paragraph {future_to_key[future]} timed out")
            except Exception as e:
                logging.error(f"Error in thread execution: {e}")

    return similarity_results

def process_uploaded_pdf(uploaded_file_path, metadata_json, num_threads=4):
    client, collection = initialize_chromadb()
    if client is None or collection is None:
        raise ValueError("ChromaDB is not properly initialized. Cannot process the uploaded file.")

    metadata = load_metadata(metadata_json)
    text_pages = extract_text_from_pdf(uploaded_file_path)
    paragraphs = split_into_paragraphs(text_pages)

    # Summarize the uploaded PDF content
    full_text = " ".join(text_pages)
    summary = summarizing_using_gemini(full_text)

    # Query ChromaDB for similarities
    results = query_chromadb(collection, summary, top_n=5)
    
    # Debugging: Check the structure of results
    logging.info(f"Results: {results}")
    
    similarities = []
    citations = []

    # Extract the inner list from distances
    distances = results.get("distances", [[1.0] * len(results.get("metadatas", []))])[0]
    
    if not isinstance(distances, list):
        raise ValueError("Expected 'distances' to be a list of float values.")

    for i, metadata_entry in enumerate(results.get("metadatas", [])[0]):
        # Access each float value from the distances list
        try:
            similarity_score = 1 - float(distances[i])  # Convert to float to ensure compatibility
        except (IndexError, ValueError) as e:
            logging.error(f"Error accessing or converting distance at index {i}: {e}")
            continue

        reference_key = metadata_entry.get("file")

        if similarity_score >= SIMILARITY_THRESHOLD:
            similarities.append({
                "reference_file": reference_key,
                "paragraph_key": metadata_entry.get("key"),
                "similarity_score": similarity_score,
            })

            citation = format_mla_citation_from_metadata(reference_key, metadata)
            citations.append(citation)

    # Save citations to a file
    citation_file = os.path.splitext(uploaded_file_path)[0] + "_citations.txt"
    save_citations_to_file(citations, citation_file)

    return {"similarities": similarities, "citations_file": citation_file}


# def preload_reference_data(reference_folder, metadata_json, batch_size=10):
#     client, collection = initialize_chromadb()
#     model = SentenceTransformer('roberta-base')
#     metadata = load_metadata(metadata_json)

#     ref_files = [f for f in os.listdir(reference_folder) if f.endswith(".pdf")]

#     for i in range(0, len(ref_files), batch_size):
#         batch = ref_files[i:i + batch_size]
#         for ref_file in batch:
#             ref_path = os.path.join(reference_folder, ref_file)
#             logging.info(f"Processing reference file: {ref_file}")
#             text_pages = extract_text_from_pdf(ref_path)
#             paragraphs = split_into_paragraphs(text_pages)
#             try:
#                 add_reference_to_chromadb(collection, ref_file, paragraphs)
#             except Exception as e:
#                 logging.error(f"Error adding {ref_file} to ChromaDB: {e}")
#         logging.info(f"Processed batch {i // batch_size + 1}")

#     logging.info("Reference data loaded into ChromaDB!")

def preload_reference_data(reference_folder, metadata_json, batch_size=10):
    client, collection = initialize_chromadb()
    if client is None or collection is None:
        logging.error("ChromaDB initialization failed. Cannot preload data.")
        return

    model = SentenceTransformer('all-MiniLM-L6-v2')  # Ensure you're using a valid model
    metadata = load_metadata(metadata_json)
    
    ref_files = [f for f in os.listdir(reference_folder) if f.endswith(".pdf")]
    
    for i in range(0, len(ref_files), batch_size):
        batch = ref_files[i:i + batch_size]
        for ref_file in batch:
            ref_path = os.path.join(reference_folder, ref_file)
            logging.info(f"Processing reference file: {ref_file}")
            text_pages = extract_text_from_pdf(ref_path)
            paragraphs = split_into_paragraphs(text_pages)
            
            try:
                # Pass collection explicitly
                add_reference_to_chromadb(collection, ref_file, paragraphs)
            except Exception as e:
                logging.error(f"Error adding {ref_file} to ChromaDB: {e}")
        
        logging.info(f"Processed batch {i // batch_size + 1}")
    
    logging.info("Reference data loaded into ChromaDB!")