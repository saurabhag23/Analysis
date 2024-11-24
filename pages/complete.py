import streamlit as st
import requests

# Set the backend URL where the analysis data is fetched
BACKEND_URL = "http://localhost:8000"

def fetch_complete_data(ticker):
    """Fetches complete analysis data (both fundamental and technical) from the backend."""
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type=both")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch complete data for {ticker}: HTTP Status Code {response.status_code}")
        return None

def app():
    """Main function for the Streamlit application."""
    st.set_page_config(page_title="Complete Analysis", layout="wide")
    st.title('Complete Analysis')

    ticker = st.text_input('Enter the stock ticker for complete analysis (e.g., AAPL):', '')

    if ticker:
        if st.button('Analyze Completely'):
            data = fetch_complete_data(ticker)
            if data:
                # Displaying the complete analysis data
                st.subheader(f"Complete Analysis for {ticker}")
                st.json(data)  # Display data as JSON for simplicity
            else:
                st.error("Failed to fetch or display complete analysis data.")

if __name__ == "__main__":
    app()
