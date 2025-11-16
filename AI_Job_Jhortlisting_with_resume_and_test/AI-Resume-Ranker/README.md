
# AI Resume Shortlisting System

This project takes a **Job Description (JD)** and multiple **resumes** as input and:
- Rejects resumes missing mandatory JD requirements (or below threshold).
- Scores accepted resumes using skill match, experience, education, and grades.
- Ranks resumes and outputs top-N shortlisted candidates.

## Quick start (tested with Python 3.10+)

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place plain-text resumes into `resumes/` (supported: `.txt`, `.pdf`, `.docx`).
   Example resumes are provided.

4. Edit `job_description.txt` to enter the JD. To mark **mandatory** skills, put them on a line starting with:
   `Required:` or `MANDATORY:` (comma-separated). E.g.
   ```
   Required: Python, Machine Learning, SQL
   ```

5. Run the ranker and get top-`N` results:
   ```bash
   python main.py --top 5
   ```

6. Output is saved to `output/ranked_resumes.csv`.

## Project structure

```
AI-Resume-Ranker/
├── main.py
├── requirements.txt
├── job_description.txt
├── resumes/
├── output/
└── utils/
    ├── extract_text.py
    ├── extract_features.py
    └── ranker.py
```

## Notes

- The project uses a simple, robust approach (keyword matching + TF-IDF fallback) so it runs without heavy NLP models.
- For better parsing of PDFs and DOCX, ensure `PyPDF2` and `python-docx` are installed (already in requirements).
- Feel free to add more skills to `utils/skills.txt` if your domain needs additional keywords.

