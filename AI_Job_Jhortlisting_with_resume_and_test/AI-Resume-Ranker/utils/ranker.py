
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def skill_match_score(candidate_skills, jd_required, jd_text=None):
    # If required skills explicitly provided, compute fraction matched
    if jd_required:
        if len(jd_required) == 0:
            return 1.0
        matched = 0
        for s in jd_required:
            # simple substring match in candidate skills
            if any(s in cs for cs in candidate_skills):
                matched += 1
        return matched / len(jd_required)
    # fallback: if no required list, use candidate skill count against jd_text using simple tfidf similarity
    if jd_text and len(candidate_skills) > 0:
        docs = [' '.join(candidate_skills), jd_text]
        vec = TfidfVectorizer().fit_transform(docs)
        sims = (vec * vec.T).A
        return float(sims[0,1])
    return 0.0

def normalize_experience(exp_years, max_years=20):
    return min(exp_years / max_years, 1.0)

def rank_resumes(candidates, jd_info, top_n=None, skill_weight=0.5, exp_weight=0.3, edu_weight=0.1, grade_weight=0.1, reject_threshold=0.6):
    jd_required = jd_info.get('required_skills', [])
    jd_text = jd_info.get('text','')

    scored = []
    for c in candidates:
        s_score = skill_match_score(c.get('skills',[]), jd_required, jd_text)
        e_score = normalize_experience(c.get('experience_years',0))
        edu_score = 0.0
        if 'education_level' in c:
            edu_map = {'phd':1.0, 'masters':0.8, 'bachelors':0.6, 'diploma':0.4, 'unknown':0.3}
            edu_score = edu_map.get(c['education_level'], 0.3)
        g_score = c.get('grade_score', 0.5)

        total = skill_weight*s_score + exp_weight*e_score + edu_weight*edu_score + grade_weight*g_score

        # rejection logic
        rejected = False
        if jd_required:
            # require full match of mandatory skills (strict) or at least 60%?
            # We'll reject if skill match < reject_threshold
            if s_score < reject_threshold:
                rejected = True
        else:
            if s_score < 0.2:
                rejected = True

        scored.append({
            'name': c.get('name','unknown'),
            'file_path': c.get('file_path',''),
            'skills_found': ', '.join(c.get('skills',[])),
            'skill_match': round(s_score,3),
            'experience_years': c.get('experience_years',0),
            'education_level': c.get('education_level','unknown'),
            'grade_score': round(g_score,3),
            'total_score': round(total,3),
            'rejected': rejected
        })

    # only accepted
    accepted = [s for s in scored if not s['rejected']]
    accepted.sort(key=lambda x: x['total_score'], reverse=True)
    
    #  handle top_n=None
    if top_n is None:
        print(f"🏁 Returning all {len(accepted)} resumes (no top_n limit)")
        return accepted

    print(f"🏁 Returning top {top_n} resumes out of {len(accepted)}")
    return accepted[:top_n]
