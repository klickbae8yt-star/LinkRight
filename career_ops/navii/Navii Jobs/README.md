# Navii Jobs - Resume Screening Pipeline

## Directory Structure

```
Navii Jobs/
├── auth/                    # Authentication state files
│   └── _auth_state.json     # Google Drive login session
│
├── data/                    # Input data files
│   ├── #ApplyToAmex - Form Responses 1.csv  # Source CSV with 2,344 candidates
│   ├── all_resumes.md       # Extracted resume text (2,277 valid)
│   ├── navii_jobs_complete.md  # 14 job descriptions + evaluation criteria
│   ├── navii_jobs.csv       # Job card data export
│   ├── _extract_progress.json  # Extraction progress tracking
│   └── Vinyl equity/        # Additional job data
│
├── scripts/                 # Python scripts
│   ├── extract_resumes.py   # Playwright extraction (main script)
│   ├── retry_failed.py      # Retry failed extractions
│   ├── login_save.py        # Refresh Google auth state
│   └── evaluate_candidates.py  # Keyword-based scoring (14 roles)
│
├── output/                  # Results
│   └── evaluation_results.csv  # Scores for all candidates × 14 roles
│
└── chatgpt_eval/            # ChatGPT batch evaluation (future)
    ├── prompts/
    ├── batches/
    └── results/
```

## Quick Start

### 1. Extract Resumes
```bash
cd "Navii Jobs"
python3 scripts/login_save.py  # First time only
python3 scripts/extract_resumes.py
```

### 2. Retry Failed
```bash
python3 scripts/retry_failed.py --max 10  # Test first
python3 scripts/retry_failed.py            # Full retry
```

### 3. Evaluate Candidates
```bash
python3 scripts/evaluate_candidates.py
```

## Status
- **Extracted**: 2,277 / 2,344 candidates (97.1%)
- **Evaluated**: 2,343 candidates across 14 roles
- **Output**: `evaluation_results.csv` sorted by total score
