# dashboard.py
import streamlit as st
import pandas as pd

# ─── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce ETL Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ─── Load Data from CSV ───────────────────────────────
@st.cache_data
def load_data():
    import os
    base_path = os.path.dirname(__file__)
    filepath = os.path.join(base_path, "data", "clean_data.csv")
    orders = pd.read_csv(filepath, low_memory=False)
    orders['InvoiceDate'] = pd.to_datetime(orders['InvoiceDate'])
    orders['Is_Cancelled'] = orders['Is_Cancelled'].astype(str) == 'True'
    cancellations = orders[orders['Is_Cancelled'] == True]
    summary = orders[orders['Is_Cancelled'] == False].groupby('Country').agg(
        Total_Orders     = ('InvoiceNo',  'nunique'),
        Total_Revenue    = ('TotalPrice', 'sum'),
        Total_Quantity   = ('Quantity',   'sum'),
        Unique_Customers = ('CustomerID', 'nunique')
    ).reset_index()
    summary['Total_Revenue'] = summary['Total_Revenue'].round(2)
    return orders, summary, cancellations

# ─── Title ────────────────────────────────────────────
st.title("🛒 E-Commerce Sales Dashboard")
st.markdown("**Data Source:** UK E-Commerce Dataset | **Pipeline:** Python + MySQL ETL")
st.divider()

# ─── KPI Cards ────────────────────────────────────────
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

normal_orders = orders[orders['Is_Cancelled'] == False]
total_revenue     = normal_orders['TotalPrice'].sum()
total_orders      = normal_orders['InvoiceNo'].nunique()
total_customers   = normal_orders['CustomerID'].nunique()
cancellation_rate = len(cancellations) / len(orders) * 100

col1.metric("Total Revenue",     f"£{total_revenue:,.2f}")
col2.metric("Total Orders",      f"{total_orders:,}")
col3.metric("Total Customers",   f"{total_customers:,}")
col4.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")

st.divider()

# ─── Monthly Revenue Chart ────────────────────────────
st.subheader("Monthly Revenue Trend")
monthly = normal_orders.groupby(['Year', 'Month'])['TotalPrice'].sum().reset_index()
monthly['Date'] = pd.to_datetime(monthly[['Year', 'Month']].assign(Day=1))
monthly = monthly.sort_values('Date')
st.line_chart(monthly.set_index('Date')['TotalPrice'])

st.divider()

# ─── Top 10 Countries ─────────────────────────────────
st.subheader("Top 10 Countries by Revenue")
top10 = summary.nlargest(10, 'Total_Revenue')[['Country', 'Total_Revenue']]
st.bar_chart(top10.set_index('Country'))

st.divider()

# ─── Two Columns Layout ───────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Products")
    top_products = normal_orders.groupby('Description')['TotalPrice']\
        .sum().nlargest(10).reset_index()
    top_products.columns = ['Product', 'Revenue']
    st.dataframe(top_products, use_container_width=True)

with col2:
    st.subheader("Orders by Day of Week")
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dow = normal_orders['Day_of_week'].value_counts().reindex(day_order)
    st.bar_chart(dow)

st.divider()

# ─── Country Summary Table ────────────────────────────
st.subheader("Full Country Summary")
st.dataframe(
    summary.sort_values('Total_Revenue', ascending=False),
    use_container_width=True
)

st.divider()

# ─── Raw Data Explorer ────────────────────────────────
st.subheader("Raw Data Explorer")
country_filter = st.selectbox(
    "Filter by Country:",
    ["All"] + sorted(orders['Country'].unique().tolist())
)

if country_filter == "All":
    st.dataframe(orders.head(100), use_container_width=True)
else:
    filtered = orders[orders['Country'] == country_filter]
    st.dataframe(filtered.head(100), use_container_width=True)