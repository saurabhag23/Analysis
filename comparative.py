import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Constants
BACKEND_URL = "http://localhost:8000"  # Adjust if hosted differently

def display_comparative_analysis():
    st.header("Comparative Analysis")

    # User input for multiple stock tickers
    tickers = st.multiselect('Select stock tickers for comparison:', ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'], default=['AAPL', 'MSFT'])

    # User selection for type of data to compare
    data_type = st.selectbox('Select the type of data to compare:', ['Fundamental', 'Technical'])

    # Button to fetch and display data
    if st.button('Compare Stocks'):
        if tickers:
            comparative_data = {ticker: fetch_data(ticker, data_type.lower()) for ticker in tickers}
            display_comparative_data(comparative_data, data_type)

def fetch_data(ticker, analysis_type):
    """Fetch data based on analysis type for a given ticker."""
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type={analysis_type}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch {analysis_type} data for {ticker}: HTTP Status Code {response.status_code}")
        return None

def display_comparative_data(data, data_type):
    """Display comparative data for selected stocks and data type."""
    if data_type == 'Fundamental':
        metric = 'pe_ratio'  # Example: Comparing P/E ratios, can add more metrics
        df = pd.DataFrame({
            ticker: [details.get(metric, None) for details in metrics.values()]
            for ticker, metrics in data.items()
        }, index=[metric])
        st.write(f"Comparative {metric}")
        st.bar_chart(df)
    elif data_type == 'Technical':
        # Example: Comparing Simple Moving Averages
        fig = px.line(
            {ticker: pd.DataFrame(metrics['SMA']) for ticker, metrics in data.items() if 'SMA' in metrics},
            x='Date',
            y='Value',
            title='Comparative SMA'
        )
        st.plotly_chart(fig)

if __name__ == "__main__":
    display_comparative_analysis()
