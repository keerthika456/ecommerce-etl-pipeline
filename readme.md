# E-Commerce ETL Pipeline

## Overview
End-to-end ETL pipeline built with Python and MySQL
that processes 541,909 UK e-commerce transactions.

## Live Dashboard
👉https://ecommerce-etl-pipeline-mhs3jmfezgykwmgw5nxm4o.streamlit.app/

## GitHub
👉 https://github.com/keerthika456/ecommerce-etl-pipeline

## Tech Stack
- Python 3.14
- Pandas
- SQLAlchemy
- MySQL
- Streamlit

## Project Structure
etl_project/
├── extract.py       # Reads CSV data
├── transform.py     # Cleans and enriches data
├── load.py          # Loads to MySQL
├── pipeline.py      # Orchestrates ETL
├── dashboard.py     # Streamlit dashboard
├── config.py        # Configuration
├── logger.py        # Logging setup
└── requirements.txt

## Pipeline Steps
1. Extract   → Loads 541,909 rows from CSV
2. Transform → Cleans data, fixes types, flags cancellations
3. Load      → Creats 3 tables in MySQL

## Tables Created
| Table | Rows | Description |
|-------|------|-------------|
| orders | 536,639 | All cleaned orders |
| cancellations | 10,587 | Cancelled orders |
| country_summary | 38 | Revenue by country |

## Key Findings
- Total Revenue: £10,642,110
- Total Orders: 20,726
- Total Customers: 4,340
- Cancellation Rate: 2.0%
- Countries Served: 38

## How to Run
1. Clone the repo
2. Install requirements:
   pip install -r requirements.txt
3. Create .env file with DB credentials:
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=etl_project
   FILE_PATH=data/data.csv
4. Run pipeline:
   python pipeline.py
5. Run dashboard:
   streamlit run dashboard.py