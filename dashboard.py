import streamlit as st
import requests

# Constants
BACKEND_URL = "http://localhost:8000"

def main():
    st.set_page_config(layout="wide", page_title="Advanced Investment Analyst Dashboard")
    st.title('Advanced Investment Analyst Dashboard')

    ticker = st.text_input('Enter the stock ticker (e.g., AAPL):', value='AAPL')

    # Initialize or reset analysis state
    if 'analysis_type' not in st.session_state or st.button('Reset'):
        st.session_state['analysis_type'] = None

    if st.button('Show Overview') or st.session_state['analysis_type'] == 'overview':
        overview_data = fetch_data(ticker, 'overview')
        if overview_data:
            display_overview(overview_data)
            st.session_state['analysis_type'] = 'overview'  # Mark state as overview shown
            show_analysis_buttons(ticker)
        else:
            st.error("Failed to fetch overview data.")

def fetch_data(ticker, analysis_type):
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type={analysis_type}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data for {ticker}: HTTP Status Code {response.status_code}")
        return None

def display_overview(data):
    st.subheader('Stock Overview')
    st.write(f"Price: ${data.get('price', 'N/A')}")
    st.write(f"Market Cap: {data.get('market_cap', 'N/A')}")
    st.write(f"P/E Ratio: {data.get('pe_ratio', 'N/A')}")
    st.write(f"Dividend Yield: {data.get('dividend_yield', 'N/A')}%")

def show_analysis_buttons(ticker):
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Fundamental Analysis'):
            st.session_state['analysis_type'] = 'fundamental'
            fetch_and_display(ticker, 'fundamental')
    with col2:
        if st.button('Technical Analysis'):
            st.session_state['analysis_type'] = 'technical'
            fetch_and_display(ticker, 'technical')
    with col3:
        if st.button('Complete Analysis'):
            st.session_state['analysis_type'] = 'both'
            fetch_and_display(ticker, 'complete')

def fetch_and_display(ticker, analysis_type):
    data = fetch_data(ticker, analysis_type)
    if data:
        st.subheader(f'{analysis_type.capitalize()} Analysis Results')
        st.json(data)
    else:
        st.error(f"No {analysis_type} data available.")

if __name__ == "__main__":
    main()
