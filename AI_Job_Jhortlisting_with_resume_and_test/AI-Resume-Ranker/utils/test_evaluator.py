import os, json, csv
from typing import List, Dict

# Defaults
MIN_TIME_MCQ = 8
MIN_TIME_CODING = 300
MCQ_TOTAL_MARKS = 20
CODING_TOTAL_MARKS = 30

DEFAULT_TEST = {
    "mcq_answers": {
        "mcq1": "B", "mcq2": "A", "mcq3": "D", "mcq4": "C",
        "mcq5": "B", "mcq6": "A", "mcq7": "C", "mcq8": "B",
        "mcq9": "D", "mcq10": "A"
    },
    "coding_answers": {
        "code1": {"expected_output": "42"},
        "code2": {"expected_output": "hello world"},
        "code3": {"expected_output": "sorted"}
    }
}

def _to_int_safe(x, default=0):
    try:
        if x is None:
            return default
        return int(x)
    except:
        return default

def load_test(definition_path: str = None):
    if definition_path and os.path.exists(definition_path):
        with open(definition_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_TEST

def evaluate_candidate(resp: Dict, test_def: Dict, min_time_mcq: int, min_time_coding: int, resume_score: float = 0.0):
    reasons = []
    cheated = False
    mcq_score = 0
    coding_score = 0

    # MCQs
    mcq_answers_ref = test_def.get('mcq_answers', {})
    mcq_resp = resp.get('mcq', {}) or {}
    for qid, correct in mcq_answers_ref.items():
        r = mcq_resp.get(qid, {})
        ans = r.get('answer')
        t = _to_int_safe(r.get('time_spent', 0))
        attempted = ans is not None and ans.lower() != "none"
        if attempted and t < min_time_mcq:
            cheated = True
            reasons.append(f"Cheated on MCQ {qid} (time {t}s < {min_time_mcq}s)")
        if attempted and str(ans).strip().upper() == str(correct).strip().upper():
            mcq_score += MCQ_TOTAL_MARKS / len(mcq_answers_ref)

    # Coding
    coding_answers_ref = test_def.get('coding_answers', {})
    coding_resp = resp.get('coding', {}) or {}
    for qid, ref in coding_answers_ref.items():
        r = coding_resp.get(qid, {})
        out = r.get('output')
        t = _to_int_safe(r.get('time_spent', 0))
        attempted = bool(r.get('attempted', False)) or (out is not None)
        if attempted and t < min_time_coding:
            cheated = True
            reasons.append(f"Cheated on coding {qid} (time {t}s < {min_time_coding}s)")
        expected = ref.get('expected_output')
        if attempted and str(out).strip() == str(expected).strip():
            coding_score += CODING_TOTAL_MARKS / len(coding_answers_ref)

    test_score = mcq_score + coding_score
    test_percent = test_score / (MCQ_TOTAL_MARKS + CODING_TOTAL_MARKS)
    combined_percent = (resume_score + test_percent) / 2

    return {
        "test_score": test_score,
        "test_percent": test_percent,
        "resume_percent": resume_score,
        "combined_percent": combined_percent,
        "cheated": cheated,
        "reasons": reasons
    }

def evaluate_folder(responses_folder: str, test_def: Dict, min_time_mcq: int, min_time_coding: int, ranked_resume_path: str = None):
    selected = []
    rejected = []
    all_ranked = []

    # Load resume scores once
    resume_scores = {}
    if ranked_resume_path and os.path.exists(ranked_resume_path):
        with open(ranked_resume_path, 'r', encoding='utf-8') as rf:
            reader = csv.DictReader(rf)
            for r in reader:
                file_name = os.path.splitext(os.path.basename(r['file_path']))[0]
                resume_scores[file_name.lower()] = float(r.get('total_score', 0))

    for fname in os.listdir(responses_folder):
        if not fname.lower().endswith('.json'):
            continue
        fpath = os.path.join(responses_folder, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                resp = json.load(f)
        except Exception as e:
            all_ranked.append({
                "filename": fname,
                "candidate_name": os.path.splitext(fname)[0],
                "cheated": True,
                "selected": False,
                "reasons": [f"Invalid JSON: {e}"],
                "resume_percent": 0,
                "test_score": 0,
                "test_percent": 0,
                "combined_percent": 0
            })
            continue

        # get resume score by filename
        resume_score = resume_scores.get(os.path.splitext(fname)[0].lower(), 0.0)
        result = evaluate_candidate(resp, test_def, min_time_mcq, min_time_coding, resume_score)

        candidate_dict = {
            "filename": fname,
            "candidate_name": resp.get('candidate_name') or os.path.splitext(fname)[0],
            "resume_percent": result['resume_percent'],
            "test_score": result['test_score'],
            "test_percent": result['test_percent'],
            "combined_percent": result['combined_percent'],
            "cheated": result['cheated'],
            "selected": not result['cheated'],
            "reasons": "; ".join(result['reasons'])
        }

        all_ranked.append(candidate_dict)
        if result['cheated']:
            rejected.append(candidate_dict)
        else:
            selected.append(candidate_dict)

    # sort descending by combined_percent
    all_ranked.sort(key=lambda x: x['combined_percent'], reverse=True)
    return selected, rejected, all_ranked

def save_ranked_results(selected, rejected, all_ranked, out_folder):
    os.makedirs(out_folder, exist_ok=True)
    sel_path = os.path.join(out_folder, 'selected_candidates.csv')
    rej_path = os.path.join(out_folder, 'rejected_candidates.csv')
    ranked_path = os.path.join(out_folder, 'all_ranked_candidates.csv')

    # Sort selected by combined_percent descending and add rank
    selected_sorted = sorted(selected, key=lambda x: x['combined_percent'], reverse=True)
    for idx, s in enumerate(selected_sorted, start=1):
        s['rank'] = idx

    # Sort rejected by combined_percent descending and add rank
    rejected_sorted = sorted(rejected, key=lambda x: x['combined_percent'], reverse=True)
    for idx, r in enumerate(rejected_sorted, start=1):
        r['rank'] = idx

    # Selected CSV
    with open(sel_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['rank', 'candidate_name', 'reasons', 'combined_percent'])
        for s in selected_sorted:
            writer.writerow([s['rank'], s['candidate_name'], s['reasons'], round(s['combined_percent'], 4)])

    # Rejected CSV
    with open(rej_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['rank', 'candidate_name', 'reasons', 'combined_percent'])
        for r in rejected_sorted:
            writer.writerow([r['rank'], r['candidate_name'], r['reasons'], round(r['combined_percent'], 4)])

    # All ranked (already sorted in evaluate_folder)
    with open(ranked_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['rank','filename','candidate_name','resume_percent','test_score','test_percent','combined_percent','cheated','selected','reasons'])
        for idx, r in enumerate(all_ranked, start=1):
            writer.writerow([idx, r['filename'], r['candidate_name'], r['resume_percent'], r['test_score'],
                             r['test_percent'], r['combined_percent'], r['cheated'], r['selected'], r['reasons']])
    return sel_path, rej_path, ranked_path
