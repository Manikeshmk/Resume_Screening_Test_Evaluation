#python evaluate_tests.py --responses responses --shortlist output/ranked_resumes.csv --out output/test_results

import argparse
import os
from utils.test_evaluator import load_test, evaluate_folder, save_ranked_results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--responses', required=True, help='Folder containing candidate JSON responses')
    parser.add_argument('--shortlist', required=False, help='CSV file of ranked resumes')
    parser.add_argument('--out', required=True, help='Output folder')
    parser.add_argument('--min_mcq', type=int, default=8, help='Minimum MCQ time threshold (seconds)')
    parser.add_argument('--min_code', type=int, default=300, help='Minimum coding time threshold (seconds)')
    parser.add_argument('--test_def', required=False, help='JSON file defining test answers')

    args = parser.parse_args()

    test_def = load_test(args.test_def)
    selected, rejected, all_ranked = evaluate_folder(
        responses_folder=args.responses,
        test_def=test_def,
        min_time_mcq=args.min_mcq,
        min_time_coding=args.min_code,
        ranked_resume_path=args.shortlist
    )

    sel_path, rej_path, ranked_path = save_ranked_results(selected, rejected, all_ranked, args.out)
    print(f"Selected saved to: {sel_path}")
    print(f"Rejected saved to: {rej_path}")
    print(f"All ranked saved to: {ranked_path}")
    print(f"Selected count: {len(selected)} Rejected count: {len(rejected)} Total ranked: {len(all_ranked)}")

if __name__ == '__main__':
    main()
