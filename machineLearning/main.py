from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import shutil
import logging
from service import preload_reference_data, process_uploaded_pdf
from chromadb_service import initialize_chromadb

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(debug=True)

# Configurations
REFERENCE_FOLDER = "./test_docs"
UPLOADED_FOLDER = "./uploaded"
RESULTS_FOLDER = "./results"
METADATA_JSON = "../DocsInfo/pdfinfo.json"

# Ensure directories exist
os.makedirs(REFERENCE_FOLDER, exist_ok=True)
os.makedirs(UPLOADED_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.on_event("startup")
def startup_event():
    """Preload reference PDFs into ChromaDB."""
    try:
        client, collection = initialize_chromadb()
        if client is None or collection is None:
            raise ValueError("Failed to initialize ChromaDB. Check the database configuration.")
        preload_reference_data(REFERENCE_FOLDER, METADATA_JSON)
        logging.info("Successfully preloaded reference data into ChromaDB.")
    except Exception as e:
        logging.error(f"Error during startup preload: {e}")
    
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Accept an uploaded PDF, compare it with reference data, and generate MLA citations.
    """
    uploaded_file_path = os.path.join(UPLOADED_FOLDER, file.filename)
    
    try:
        # Save the uploaded file
        with open(uploaded_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        logging.info(f"Uploaded file saved to {uploaded_file_path}")

        # Process the uploaded PDF
        result = process_uploaded_pdf(uploaded_file_path, METADATA_JSON)

        # Prepare the response
        response = {
            "similarities": result["similarities"],
            "citation_file": result["citations_file"],
        }

        # Optionally, include the contents of the citations file in the response
        try:
            with open(result["citations_file"], "r", encoding="utf-8") as f:
                citations_content = f.read()
            response["citations"] = citations_content
        except Exception as e:
            logging.error(f"Error reading citations file: {e}")
            response["citations"] = "Error reading citations file."

        return JSONResponse(response)

    except Exception as e:
        logging.error(f"Error processing uploaded file: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
