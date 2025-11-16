from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil, os
from typing import List
from main import process_resumes  # import the pipeline

app = FastAPI()

# Allow React to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_resumes(resumes: List[UploadFile] = File(...)):
    """Receive multiple resumes, store them, run ranking, return top results."""

    saved_files = []
    for resume in resumes:
        file_path = os.path.join(UPLOAD_DIR, resume.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        saved_files.append(file_path)
        print(f"✅ Saved: {file_path}")

    # Run ranking pipeline on all resumes in folder
    df = process_resumes(
        resume_folder=UPLOAD_DIR,
        jd_file="job_description.txt",
        top_n=None,
        output="output/ranked_resumes.csv",
    )

    # Sort all results
    df_sorted = df.sort_values(by="total_score", ascending=False)

    # Mark which ones were just uploaded
    df_sorted["uploaded"] = df_sorted["file_path"].apply(
        lambda p: os.path.abspath(p) in [os.path.abspath(f) for f in saved_files]
    )

    # Top N for display
    top_n = 5
    top_resumes = df_sorted.head(top_n).to_dict(orient="records")

    # Uploaded resumes (with their rank or rejection)
    uploaded_results = []
    for file_path in saved_files:
        uploaded_abs = os.path.abspath(file_path)
        match = df_sorted[df_sorted["file_path"].apply(lambda p: os.path.abspath(p) == uploaded_abs)]
        if not match.empty:
            record = match.to_dict(orient="records")[0]
            record["rejected"] = record.get("rejected", False)
            uploaded_results.append(record)
        else:
            uploaded_results.append({
                "name": os.path.basename(file_path),
                "file_path": uploaded_abs,
                "rejected": True,
                "message": "This resume was rejected or not found in results"
            })

    print(f"🏁 Processed {len(saved_files)} uploaded resumes.")
    return {
        "status": "success",
        "uploaded_resumes": uploaded_results,
        "top_resumes": top_resumes,
    }