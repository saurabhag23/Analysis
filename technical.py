import streamlit as st
import requests
import urllib.parse

def fetch_technical_data(ticker):
    BACKEND_URL = "http://localhost:8000"  # Adjust if hosted differently
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type=technical")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch technical data for {ticker}: HTTP Status Code {response.status_code}")
        return {}

def main():
    st.set_page_config(layout="wide", page_title="Technical Analysis Results")
    st.title('Technical Analysis Results')

    # Parsing ticker from URL query parameter
    query_params = st.experimental_get_query_params()
    ticker = query_params.get('ticker', [''])[0]

    if ticker:
        st.subheader(f"Technical Analysis for {ticker}")
        data = fetch_technical_data(ticker)
        if data:
            st.json(data)
        else:
            st.error("No technical data available.")
    else:
        st.error("No ticker provided. Please provide a ticker symbol in the URL query parameter.")

if __name__ == "__main__":
    main()
