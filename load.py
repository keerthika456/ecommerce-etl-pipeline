import pandas as pd
from sqlalchemy import create_engine, text
from config import CONNECTION_STRING
from logger import logger

def load(df: pd.DataFrame):
    """
    Loads cleaned data into MySQL database.
    Creates 3 tables:
    1. orders          → all cleaned data
    2. cancellations   → cancelled orders only
    3. country_summary → sales summary by country
    """
    try:
        #----------------1.Create DB connection-------------------------
        engine = create_engine(CONNECTION_STRING)

        #----------------2.Test DB connection---------------------------
        with engine.connect() as conn:
            conn.execute(text("select 1"))
        logger.info("[Load] Database connection successful")

        #----------------3.Load Main Order Table------------------------
        df.to_sql(name = "orders", con = engine, if_exists = "replace", index =  False)
        logger.info(f"[Load] {len(df):,} rows loaded into table: orders")

        #----------------4.Load Cancellation Table------------------------
        cancelled_df = df[df['Is_Cancelled'] == True]
        cancelled_df.to_sql(name = "cancellations", con = engine, if_exists = "replace", index =  False)
        logger.info(f"[Load] {len(cancelled_df):,} rows loaded into table: cancellation")

        # ----------------5.Load Country Summary Table--------------------
        summary_df = df[df['Is_Cancelled'] == False].groupby('Country').agg(
            Total_Orders   = ('InvoiceNo',  'nunique'),
            Total_Revenue  = ('TotalPrice', 'sum'),
            Total_Quantity = ('Quantity',   'sum'),
            Unique_Customers = ('CustomerID', 'nunique')
        ).reset_index()

        summary_df['Total_Revenue'] = summary_df['Total_Revenue'].round(2)

        summary_df.to_sql(name = "country_summary", con = engine, if_exists = "replace", index =  False)
        logger.info(f"[Load] {len(summary_df):,} rows loaded into table: country_summary")
        logger.info("[Load] All done!")

    except Exception as e:
        logger.error(f"[Load] Failed {e}")
        raise




