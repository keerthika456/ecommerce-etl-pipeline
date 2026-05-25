import pandas as pd
from logger import logger

def extract(filepath: str) -> pd.DataFrame:
    """
    Reads the CSV file and returns a raw DataFrame.
    """
    try:
         df = pd.read_csv(filepath, encoding='latin-1')
         logger.info(f"[Extract] {len(df)} rows loaded from {filepath}")
         return df 
    except FileNotFoundError:
        logger.error(f"[Extract] file does not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"[Extract] unexpected error occured {e}")
        raise

