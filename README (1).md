# Springer Capital – Data Engineer Assessment

**Author:** Madiha Maheen  
**Project:** Referral Program Data Pipeline & Fraud Detection

---

## Project Overview

This project builds a data pipeline that processes referral program data for Springer Capital. It:
- Loads and profiles all source CSV tables
- Cleans and transforms the data (timezone conversion, null handling, string formatting)
- Applies business logic to detect potentially fraudulent referral rewards
- Outputs a final report (`referral_report.csv`) with a validity flag per referral

---

## Repository Structure

```
springer-data-engineer-test/
│
├── data/                   # Source CSV files (input data)
│   ├── lead_logs.csv
│   ├── user_referrals.csv
│   ├── user_referral_logs.csv
│   ├── user_logs.csv
│   ├── user_referral_statuses.csv
│   ├── referral_rewards.csv
│   └── paid_transactions.csv
│
├── output/                 # Generated report output
│   └── referral_report.csv
│
├── profiling/              # Data profiling results
│
├── your_script.py          # Main data pipeline script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container configuration
└── README.md               # This file
```

---

## How to Run (Two Options)

### Option 1: Run Locally with Python

#### Step 1 – Make sure Python 3.10+ is installed
```bash
python --version
```

#### Step 2 – Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 3 – Run the script
```bash
python your_script.py
```

#### Step 4 – Check the output
The report will be saved at:
```
output/referral_report.csv
```

---

### Option 2: Run with Docker (Recommended)

Docker ensures the script runs in a clean, consistent environment without worrying about your local Python setup.

#### Prerequisites
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Make sure Docker is running before proceeding

#### Step 1 – Build the Docker image
Open a terminal in the project root folder and run:
```bash
docker build -t springer-pipeline .
```
This creates a Docker image named `springer-pipeline`.

#### Step 2 – Run the container and export the output
```bash
docker run --rm -v "$(pwd)/output:/app/output" springer-pipeline
```

**What this does:**
- Runs the container
- Mounts your local `output/` folder so the report file is saved directly to your machine
- Automatically removes the container after it finishes (`--rm`)

> **Windows users** – use this instead:
> ```bash
> docker run --rm -v "%cd%/output:/app/output" springer-pipeline
> ```

#### Step 3 – Check the output
After the container finishes, you'll find the report at:
```
output/referral_report.csv
```

---

## Output Report

The final output is `referral_report.csv` containing **46 rows**, each representing a referral with the following key columns:

| Column | Description |
|---|---|
| `referral_details_id` | Unique row ID |
| `referral_id` | Unique referral identifier |
| `referral_source` | How the referral was made |
| `referral_source_category` | Online / Offline / Lead category |
| `referral_at` | When the referral was created (local time) |
| `referrer_name` | Name of the person who referred |
| `referee_name` | Name of the new user |
| `referral_status` | Berhasil / Menunggu / Tidak Berhasil |
| `transaction_id` | Linked transaction |
| `transaction_status` | PAID or other |
| `is_business_logic_valid` | TRUE = valid referral, FALSE = potential fraud |

See `data_dictionary.xlsx` for full column descriptions for business users.

---

## Notes

- All timestamps in source data are in **UTC** and are converted to local time based on timezone fields
- No credentials are stored in the script or repository
- The `profiling/` folder contains null count and distinct value count summaries for all tables
