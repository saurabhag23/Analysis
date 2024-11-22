import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Constants
BACKEND_URL = "http://localhost:8000"  # Adjust if hosted differently

def main():
    st.set_page_config(layout="wide", page_title="Advanced Investment Analyst Dashboard")
    st.title('Advanced Investment Analyst Dashboard')

    # Sidebar for user input and navigation
    with st.sidebar:
        page = st.radio("Go to", ['Overview', 'Fundamental Analysis', 'Technical Analysis'])

    if page == 'Overview':
        display_overview()
    elif page == 'Fundamental Analysis':
        display_fundamental_analysis()
    elif page == 'Technical Analysis':
        display_technical_analysis()

def display_overview():
    ticker = st.text_input('Enter the stock ticker (e.g., AAPL):', value='AAPL')
    if st.button('Show Overview'):
        data = fetch_data(ticker, 'overview')
        if data:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Current Price", value=f"${data['price'] if data['price'] else 'N/A'}")
                st.metric(label="Market Cap", value=f"${data['market_cap']:,}")
            with col2:
                st.metric(label="P/E Ratio", value=f"{data['pe_ratio']}")
                st.metric(label="Dividend Yield", value=f"{data['dividend_yield']}%")
            with col3:
                st.metric(label="52 Week Range", value=data['52_week_range'])
        else:
            st.error("Failed to fetch overview data.")

def display_fundamental_analysis():
    ticker = st.text_input('Enter the stock ticker for fundamental analysis (e.g., MSFT):')
    if st.button('Fetch Fundamental Data'):
        data = fetch_data(ticker, 'fundamental')
        if data:
            st.json(data)
        else:
            st.error("No fundamental data available.")

def display_technical_analysis():
    ticker = st.text_input('Enter the stock ticker for technical analysis (e.g., GOOGL):')
    if st.button('Fetch Technical Data'):
        data = fetch_data(ticker, 'technical')
        if data:
            st.json(data)
        else:
            st.error("No technical data available.")


def fetch_data(ticker, analysis_type):
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type={analysis_type}")
    if response.status_code == 200:
        data = response.json()
        # Convert NaN values to None (which becomes 'null' in JSON)
        clean_data = {k: (None if pd.isna(v) else v) for k, v in data.items()}
        return clean_data
    else:
        st.error(f"Failed to fetch data for {ticker}: HTTP Status Code {response.status_code}")
        return {}

if __name__ == "__main__":
    main()
