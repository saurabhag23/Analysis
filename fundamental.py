import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Constants
BACKEND_URL = "http://localhost:8000"  # Adjust if hosted differently

def display_fundamental_analysis():
    st.header("Fundamental Analysis")
    
    # User input for stock ticker
    default_tickers = ['AAPL', 'GOOGL', 'MSFT']
    tickers = st.multiselect('Select stock ticker(s)', default_tickers, default=default_tickers[:1])

    # Button to fetch and display data
    if st.button('Analyze Stocks'):
        if tickers:
            data = {ticker: fetch_fundamental_data(ticker) for ticker in tickers}
            display_fundamental_data(data)

def fetch_fundamental_data(ticker):
    """Fetch fundamental data for a given ticker."""
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type=fundamental")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data for {ticker}: HTTP Status Code {response.status_code}")
        return None

def display_fundamental_data(data):
    """Display fundamental data for one or more stocks."""
    for ticker, metrics in data.items():
        if metrics:
            st.subheader(f"{ticker} Fundamental Metrics")
            col1, col2 = st.columns(2)
            with col1:
                st.json(metrics)  # Example: Show raw data as JSON for simplicity
            with col2:
                df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
                fig = px.bar(df, x='Metric', y='Value', title=f"{ticker} Key Financial Ratios")
                st.plotly_chart(fig)
        else:
            st.write(f"No fundamental data available for {ticker}.")

if __name__ == "__main__":
    display_fundamental_analysis()
