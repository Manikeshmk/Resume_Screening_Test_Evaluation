![Repo visits](https://hits.sh/github.com/Manikeshmk/Resume_Screening_Test_Evaluation.svg?label=repo%20visits)
![GitHub stars](https://img.shields.io/github/stars/DataScience-ArtificialIntelligence/Resume_Screening_Test_Evaluation?style=logo&logo=github&label=⭐%20Stars) 
![GitHub forks](https://img.shields.io/github/forks/DataScience-ArtificialIntelligence/Resume_Screening_Test_Evaluation?style=social)


# 🚀 AI Resume Ranker and Test Evaluator (Complete hiring process)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-Distributed%20Computing-orange?logo=apache-spark)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

*Intelligent Resume Ranking System Powered by Machine Learning & Big Data log of Test Evaluation using Apache Spark* 🤖✨
![Demo Video 2 minutes](https://github.com/DataScience-ArtificialIntelligence/Resume_Screening_Test_Evaluation/blob/main/2minutes_Video_Demo.mp4)💾💻⭐


[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Results](#-results)

</div>

---
##🤝 Team Members
- 🎓 Manikesh Kumar , 23BDS032
- 🎓 Amarjeet Raj , 23BDS006
- 🎓 Ojas Jogdand , 23BDS039
## 📋 Table of Contents

- [✨ Features](#-features)
- [📦 Prerequisites](#-prerequisites)
- [🔧 Installation](#-installation)
- [🚀 Quick Start](#-quick-start)
- [📖 Usage Guide](#-usage-guide)
- [📊 Project Structure](#-project-structure)
- [🎯 Expected Outcomes](#-expected-outcomes)
- [🔍 Cheat Detection](#-cheat-detection--bonus)
- [📝 Examples](#-examples)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

- 🎯 *Resume Ranking*: Automatically rank resumes based on job description match
- 🧠 *ML-Powered Matching*: Uses machine learning to extract and compare features
- ⚡ *Distributed Processing*: Leverages Apache Spark for large-scale data processing
- 🔎 *Cheat Detection*: Identify suspicious quiz attempts with statistical analysis
- 📊 *Data Analytics*: Comprehensive analytics on website logs and user behavior
- 🎓 *Interactive Labs*: Jupyter Notebook labs for learning Apache Spark fundamentals
- 💾 *CSV Export*: Export ranked results and analytics to CSV format

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- 🐍 *Python* >= 3.8
- ☕ *Java Development Kit (JDK)* >= 8
- 📦 *pip* (Python package manager)
- 💻 *Git*

---

## 🔧 Installation

### Step 1️⃣: Clone the Repository

```bash
git clone https://github.com/DataScience-ArtificialIntelligence/Resume_Screening_Test_Evaluation.git
cd AI-Resume-Ranker
```

### Step 2️⃣: Create a Virtual Environment

bash
# On Windows
```
python -m venv venv
venv\Scripts\activate
```

# On macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```

### Step 3️⃣: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4️⃣: Install PySpark & Additional Tools

```bash
pip install pyspark findspark
```

### Step 5️⃣: Verify Installation

```bash
python -c "import pyspark; print(f'PySpark {pyspark.__version__} installed successfully! ✅')"
```

---

## 🚀 Quick Start

### Using the Resume Ranker 📄

bash
python main.py \
  --resumes ./resumes \
  --jd job_description.txt \
  --top 5 \
  --output output/ranked_resumes.csv


### Evaluating Test Responses 📝

bash
python evaluate_tests.py \
  --responses ./responses \
  --shortlist output/ranked_resumes.csv \
  --out output/test_results \
  --min_mcq 8 \
  --min_code 300


---

## 📖 Usage Guide

### 1. Prepare Your Data 📁

*Create the following folder structure:*


AI-Resume-Ranker/
├── resumes/                      # Place resume files here (.pdf, .docx, .txt)
├── responses/                    # JSON files of candidate test responses
├── output/                       # Generated output files
├── job_description.txt           # Job description file
└── ws-logs_filtered.csv         # Website logs for analysis


### 2. Prepare Job Description 🎯

Create a job_description.txt file with the role details:


Role: Machine Learning Engineer

Responsibilities:
- Develop and deploy ML models
- Build data pipelines

Required: Python, Machine Learning, SQL
Preferred: TensorFlow, Docker, Kubernetes


### 3. Run Resume Ranking 🏃

bash
python main.py --resumes ./resumes --jd job_description.txt --top 10


### 4. Evaluate Test Responses ✅

bash
python evaluate_tests.py \
  --responses ./responses \
  --shortlist output/ranked_resumes.csv \
  --out output/test_results


### 5. Analyze Website Logs 📊

Open resume.ipynb in Jupyter Notebook for interactive Spark analytics:

bash
jupyter notebook resume.ipynb


---

## 📊 Project Structure


AI-Resume-Ranker/
│
├── 📄 main.py                          # Main resume ranking script
├── 📄 evaluate_tests.py                # Test evaluation script
├── 📓 resume.ipynb                     # Interactive Spark lab notebook
│
├── 📁 utils/
│   ├── extract_text.py                 # Extract text from PDFs/DOCX
│   ├── extract_features.py             # Feature extraction from resumes
│   ├── ranker.py                       # Ranking algorithm
│   └── test_evaluator.py               # Test evaluation logic
│
├── 📁 resumes/                         # Resume files (input)
├── 📁 responses/                       # Test response files (input)
├── 📁 output/                          # Output results
│
├── 📄 requirements.txt                 # Python dependencies
├── 📄 job_description.txt              # Job description template
├── 📄 ws-logs_filtered.csv            # Website logs data
│
├── 📄 README.md                        # This file
└── 📄 LICENSE                          # License file


---

## 🎯 Expected Outcomes

### Resume Ranking Output 📊

A CSV file (ranked_resumes.csv) with:
- ✅ Candidate name and file path
- ✅ Overall ranking score (0-100)
- ✅ Skill match percentage
- ✅ Experience level match
- ✅ Ranking position

*Example Output:*

name,file_path,score,rank
john_doe,./resumes/john_doe.pdf,95.5,1
jane_smith,./resumes/jane_smith.docx,87.3,2
bob_wilson,./resumes/bob_wilson.pdf,76.2,3


### Test Evaluation Output ✅

Three CSV files:
1. *selected_candidates.csv* - 🎉 Candidates who passed
2. *rejected_candidates.csv* - ❌ Candidates who were rejected
3. *all_ranked_candidates.csv* - 📋 Complete ranking with scores

### Cheat Detection Report 🚨

Identifies suspicious patterns:
- ⏱ *Unusually fast completion times*
- 📊 *Statistical anomalies* (< 1/5 of average time)
- 👥 *User behavior analysis*
- 📈 *Time spent on each problem*

---

## 🔍 Cheat Detection (Bonus) 🕵

The resume.ipynb notebook includes advanced cheat detection analytics:

python
# Detect cheaters based on response time anomalies
cheaters = identify_cheaters(quiz_logs, threshold=0.2)


*Detects:*
- 🏃 Suspiciously fast quiz completions
- 📝 Inadequate problem-solving time
- 🎯 Statistically improbable answer patterns
- 🔗 Collaborative behavior indicators

*Output Includes:*
- List of flagged users
- Detailed timeline analysis
- Early bird detectors
- Fastest solvers per problem

---

## 📝 Examples

### Example 1: Ranking Resumes 🎯

bash
# Basic usage
python main.py --resumes ./resumes --jd job_description.txt

# Advanced usage with custom settings
python main.py \
  --resumes /path/to/resumes \
  --jd /path/to/job_desc.txt \
  --top 15 \
  --output results/my_rankings.csv


### Example 2: Evaluating Candidates 📝

bash
python evaluate_tests.py \
  --responses ./responses \
  --shortlist output/ranked_resumes.csv \
  --out output/final_results \
  --min_mcq 5 \
  --min_code 200


### Example 3: Running Spark Analytics 🔥

Launch Jupyter and execute cells in resume.ipynb:

python
from pyspark import SparkContext
sc = SparkContext("local", "Analytics")

# Load and analyze quiz logs
logs_rdd = sc.textFile("ws-logs_filtered.csv")
# ... perform analysis


---

## 🎓 Learning Resources

### PySpark Lab Features 📚

The included Jupyter notebook (resume.ipynb) teaches:

1. *RDD Operations* 🎯
   - Creating RDDs from lists and files
   - Map, filter, flatMap transformations
   - Reduce and aggregation operations

2. *Optimizations* ⚡
   - Lazy evaluation
   - Caching and persistence
   - Checkpointing
   - Lineage tracking

3. *Spark UI* 🖥
   - Job monitoring
   - Stage analysis
   - Storage management

4. *Real-World Analytics* 📊
   - Quiz log analysis
   - Cheat detection algorithms
   - Performance metrics

---

## 🔐 Requirements

*Python Packages:*

scikit-learn          # Machine learning
pandas               # Data manipulation
PyPDF2              # PDF processing
python-docx         # DOCX processing
numpy               # Numerical computing
pyspark             # Distributed computing
findspark            # Spark initialization


---

## 🤝 Contributing

We welcome contributions! 🎉

1. *Fork* the repository 🍴
2. *Create* a feature branch (git checkout -b feature/amazing-feature)
3. *Commit* your changes (git commit -m 'Add amazing feature')
4. *Push* to the branch (git push origin feature/amazing-feature)
5. *Open* a Pull Request 🔔

---

## 🐛 Troubleshooting

### ❌ PySpark not found?
bash
pip install pyspark --upgrade
python -m pip install findspark


### ❌ Java not installed?
- Download JDK from [oracle.com](https://www.oracle.com/java/technologies/downloads/)
- Set JAVA_HOME environment variable

### ❌ Permission denied on Linux/Mac?
bash
chmod +x main.py evaluate_tests.py


### ❌ Module import errors?
bash
pip install -r requirements.txt --force-reinstall


---

## 📧 Contact & Support

- 📧 Email: 23bds032@iiitdwd.ac.in
- 🐛 Issues: [GitHub Issues](https://github.com/DataScience-ArtificialIntelligence/Resume_Screening_Test_Evaluation/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/DataScience-ArtificialIntelligence/Resume_Screening_Test_Evaluation/discussions)

---

## 📄 License

This project is licensed under the *MIT License* - see the [LICENSE](LICENSE) file for details. 📜

---

<div align="center">

### Made with ❤ by [Manikesh Kumar, Amarjeet Raj, Ojas Jogdand]

⭐ *If you found this helpful, please give it a star!* ⭐

[⬆ back to top](#-ai-resume-ranker)

</div>
