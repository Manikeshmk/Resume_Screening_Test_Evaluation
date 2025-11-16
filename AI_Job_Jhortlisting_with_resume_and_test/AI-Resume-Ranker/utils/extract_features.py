
import re, os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

SKILLS_FILE = os.path.join(os.path.dirname(__file__), 'skills.txt')

def load_skills():
    with open(SKILLS_FILE, 'r', encoding='utf-8') as f:
        return [line.strip().lower() for line in f if line.strip()]

SKILLS = load_skills()

def normalize(text):
    return text.lower()

# Extract skills by simple keyword matching
def extract_skills(text):
    txt = normalize(text)
    found = set()
    for skill in SKILLS:
        if skill in txt:
            found.add(skill)
    return sorted(found)

# Extract experience: look for patterns like "3 years", "5+ years", "experience: 4 years"
def extract_experience_years(text):
    txt = text.lower()
    patterns = [r'(\d{1,2})\s*\+?\s*years', r'(\d{1,2})\s*years?\s*of\s*experience']
    vals = []
    for pat in patterns:
        for m in re.finditer(pat, txt):
            try:
                vals.append(int(m.group(1)))
            except:
                pass
    if vals:
        return max(vals)
    # fallback: look for ranges like 2018-2023 and estimate
    years = re.findall(r'(19|20)\d{2}', txt)
    years = [int(y) for y in years]
    if years:
        return max(years) - min(years)
    return 0

# Extract education level: PhD > Masters > Bachelors > Diploma
def extract_education_level(text):
    txt = text.lower()
    if 'phd' in txt or 'ph.d' in txt:
        return 'phd'
    if 'master' in txt or 'm.tech' in txt or 'm.sc' in txt or 'msc' in txt or 'ms' in txt:
        return 'masters'
    if 'bachelor' in txt or 'b.tech' in txt or 'bsc' in txt or 'bachelor of' in txt:
        return 'bachelors'
    if 'diploma' in txt:
        return 'diploma'
    return 'unknown'

def education_score(level):
    mapping = {'phd': 1.0, 'masters': 0.8, 'bachelors': 0.6, 'diploma': 0.4, 'unknown': 0.3}
    return mapping.get(level, 0.3)

# Extract grades: look for percent or gpa
def extract_grade_score(text):
    txt = text.lower()
    # percentage
    m = re.search(r'(\d{1,3})\s*%\b', txt)
    if m:
        try:
            val = int(m.group(1))
            return min(max(val / 100.0, 0.0), 1.0)
        except:
            pass
    # gpa like 3.5/4.0
    m = re.search(r'(\d\.\d)\s*/\s*(\d\.\d)', txt)
    if m:
        try:
            g = float(m.group(1))/float(m.group(2))
            return min(max(g,0.0),1.0)
        except:
            pass
    return 0.5  # neutral if not found

def extract_features_from_text(text):
    skills = extract_skills(text)
    exp = extract_experience_years(text)
    edu = extract_education_level(text)
    grade = extract_grade_score(text)
    return {
        'skills': skills,
        'experience_years': exp,
        'education_level': edu,
        'grade_score': grade
    }

# Parse job description to find required skills (if a "Required:" line exists) otherwise derive from text
def parse_jd(text):
    txt = text.lower()
    required = []
    m = re.search(r'(required|mandatory)\s*:\s*(.*)', txt)
    if m:
        # split by comma or semicolon
        required = [s.strip() for s in re.split('[,;]', m.group(2)) if s.strip()]
    else:
        # fallback: find skills that match our SKILLS list
        for s in SKILLS:
            if s in txt:
                required.append(s)
    # dedupe and normalize
    required = sorted(set([r.lower() for r in required]))
    return {'text': text, 'required_skills': required}
