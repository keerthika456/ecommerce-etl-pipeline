import pandas as pd
from logger import logger

def transform(df: pd.DataFrame) -> pd.DataFrame:
    # This function:
    # TAKES IN  → a DataFrame (raw dirty data)
    # GIVES OUT → a DataFrame (clean data)
    """ Cleans and transforms the raw e-commerce DataFrame."""
    try:
        # 1. ---------------drop duplicates----------------------
        before = len(df)
        df = df.drop_duplicates()
        logger.info(f"[Tranform] Removed {before - len(df)} Duplicates")

        # 2.---------------Fix Column Names----------------------
        df.columns = df.columns.str.strip().str.replace(" ", "_")

        # 3.---------------Convert InvoiceDate to datetime--------------- 
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors = 'coerce') #errors='coerce' → if any date can't be converted, make it NaT (null) instead of crashing
        logger.info("[Transform] Invoicedate convered to DateTime")

        # 4. -------------Fix CustomerID from float to str----------------
        df['CustomerID'] = df['CustomerID'].fillna(0)
        df['CustomerID'] = df['CustomerID'].astype(int).astype(str)
        df['CustomerID'] = df['CustomerID'].replace("0", "Guest")
        logger.info("[Transform] CustomerID  is Cleaned")

        # 5. -------------Fill missing Description--------------------------
        df['Description'] = df['Description'].fillna("Unknown")
        logger.info("[Transform] missing Description cleaned")

        # 6. -------------Remove Negative UnitPrice--------------------------
        before = len(df)
        df = df[df["UnitPrice"] >= 0]
        logger.info(f"[Transform] Removed {before-len(df)} Negative UnitPrice Values")

        # 7. --------------Add TotalPrice column-----------------------------
        df['TotalPrice']  = df['Quantity'] * df['UnitPrice']
        logger.info("[Transform] Added TotalPrice column")

        # 8. --------------Flag_cancelled_orders-------------------------------
        df['Is_Cancelled'] = (df['Quantity'] < 0) | (df['InvoiceNo'].str.startswith('C'))
        logger.info("[Transform] cancelled order Flagged")

        # 9. --------------Add Date Parts--------------------------------------
        df['Year']= df['InvoiceDate'].dt.year
        df['Month'] = df['InvoiceDate'].dt.month
        df['Hour'] = df['InvoiceDate'].dt.hour
        df['Day_of_week'] =  df['InvoiceDate'].dt.day_name()
        logger.info("[Transform] Date Parts Extracted")

        logger.info(f"[Transform] Done - {df.shape[0]} Rows and {df.shape[1]} Columns")
        return df
    except Exception as e:
        logger.error(f"[Transform] Failed : {e}")
        raise