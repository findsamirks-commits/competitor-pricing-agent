import streamlit as st
import pandas as pd

st.set_page_config(page_title="Market Intelligence Dashboard", layout="wide")

st.title("📊 Competitor Pricing & Margin Tracker")
st.write("Live market benchmarking against internal wholesale targets.")

try:
    # Load the benchmarked data
    df = pd.read_csv("benchmarked_skus.csv")
    
    # Display high-level metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Tracked SKUs", len(df))
    
    if "Margin Delta" in df.columns:
        negative_margins = len(df[df["Margin Delta"] < 0])
        col2.metric("Pricing Risk Alerts (Negative Delta)", negative_margins)
    
    # Interactive Data Table
    st.subheader("Live SKU Economics")
    
    # Function to color code margins
    def highlight_margins(val):
        if pd.isna(val):
            return ''
        try:
            color = '#ff4b4b' if float(val) < 0 else '#00cc96'
            return f'color: {color}; font-weight: bold;'
        except ValueError:
            return ''
            
    # Apply the styling specifically to the Margin Delta column
    styled_df = df.style.map(highlight_margins, subset=['Margin Delta'])
    
    st.dataframe(styled_df, width="stretch")

except FileNotFoundError:
    st.error("No benchmark data found. Run benchmark_pipeline.py first.")