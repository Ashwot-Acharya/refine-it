from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import shutil
from service import process_uploaded_pdf, generate_citations, preload_reference_data

app = FastAPI()

REFERENCE_FOLDER = "./reference"
UPLOADED_FOLDER = "./uploaded"
RESULTS_FOLDER = "./results"

os.makedirs(REFERENCE_FOLDER, exist_ok=True)
os.makedirs(UPLOADED_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)


@app.on_event("startup")
def startup_event():
    """Preload reference PDFs into ChromaDB."""
    preload_reference_data(REFERENCE_FOLDER)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload a file and compare it with reference PDFs."""
    uploaded_file_path = os.path.join(UPLOADED_FOLDER, file.filename)

    # Save uploaded file
    with open(uploaded_file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Process uploaded PDF
    results = process_uploaded_pdf(uploaded_file_path, REFERENCE_FOLDER)

    # Generate citations for matches
    citations = generate_citations(results.keys())

    # Save results
    output_file = os.path.join(RESULTS_FOLDER, f"results_{file.filename}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(
            json.dumps({"similarities": results, "citations": citations}, indent=4)
        )

    return JSONResponse({"message": "Processing completed", "results": results, "citations": citations})
