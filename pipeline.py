
import time # built-in Python library to measure how long pipeline takes
from config import FILE_PATH
from extract import extract
from transform import transform
from load import load
from logger import logger

def run_pipeline():
    """
    Master function that runs the full ETL pipeline:
    Extract → Transform → Load
    """
    logger.info("=" * 50)
    logger.info("ETL PIPELINE STARTED")
    logger.info("=" * 50)

    start_time = time.time()

    try:
        # ─── EXTRACT ──────────────────────────────────────
        logger.info("STEP 1: EXTRACT")
        raw_df = extract(FILE_PATH)

        # ─── TRANSFORM ────────────────────────────────────
        logger.info("STEP 2: TRANSFORM")
        clean_df = transform(raw_df)

        # ─── LOAD ─────────────────────────────────────────
        logger.info("STEP 3: LOAD")
        load(clean_df)

        # ─── DONE ─────────────────────────────────────────
        elapsed = round(time.time() - start_time, 2)
        logger.info("=" * 50)
        logger.info(f"PIPELINE COMPLETED in {elapsed} seconds")
        logger.info("=" * 50)

    except Exception as e:
        logger.critical(f"PIPELINE FAILED: {e}")
          #DEBUG    → very detailed
          #INFO     → general info      ← we use this mostly
          #WARNING  → heads up
          #ERROR    → something failed
          #CRITICAL → whole system down ← pipeline failure
        raise

if __name__ == "__main__":
    run_pipeline()