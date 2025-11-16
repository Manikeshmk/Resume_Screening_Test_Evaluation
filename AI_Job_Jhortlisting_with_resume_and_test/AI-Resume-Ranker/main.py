import argparse, os
from utils.extract_text import extract_text_from_file
from utils.extract_features import extract_features_from_text, parse_jd
from utils.ranker import rank_resumes
import pandas as pd

def gather_resumes(resume_folder):
    files = []
    for name in os.listdir(resume_folder):
        if name.startswith('.'): continue
        path = os.path.join(resume_folder, name)
        if os.path.isfile(path):
            files.append(path)
    return files


def process_resumes(resume_folder='resumes', jd_file='job_description.txt', top_n=None, output='output/ranked_resumes.csv'):
    """Reusable function that runs your ranking pipeline and returns results as DataFrame."""
    with open(jd_file, 'r', encoding='utf-8') as f:
        jd_text = f.read()
    jd_info = parse_jd(jd_text)

    resume_files = gather_resumes(resume_folder)
    candidates = []
    for path in resume_files:
        text = extract_text_from_file(path)
        feats = extract_features_from_text(text)
        feats['file_path'] = path
        feats['name'] = os.path.splitext(os.path.basename(path))[0]
        candidates.append(feats)

    ranked = rank_resumes(candidates, jd_info, top_n=top_n)
    df = pd.DataFrame(ranked)
    df.to_csv(output, index=False)
    print(f"Saved top {len(df)} results to {output}")
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--resumes', default='resumes', help='Folder containing resumes')
    parser.add_argument('--jd', default='job_description.txt', help='Job description file')
    parser.add_argument('--top', type=int, default=5, help='Number of top resumes to output')
    parser.add_argument('--output', default='output/ranked_resumes.csv')
    args = parser.parse_args()

    process_resumes(args.resumes, args.jd, args.top, args.output)


if __name__ == '__main__':
    main()
