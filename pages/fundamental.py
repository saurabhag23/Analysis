import streamlit as st
import requests

# Set the backend URL where the analysis data is fetched
BACKEND_URL = "http://localhost:8000"

def fetch_fundamental_data(ticker):
    """Fetches fundamental analysis data from the backend."""
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type=fundamental")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch fundamental data for {ticker}: HTTP Status Code {response.status_code}")
        return None

def app():
    """Main function for the Streamlit application."""
    st.set_page_config(page_title="Fundamental Analysis", layout="wide")
    st.title('Fundamental Analysis')

    ticker = st.text_input('Enter the stock ticker for fundamental analysis (e.g., MSFT):', '')

    if ticker:
        if st.button('Analyze Fundamentals'):
            data = fetch_fundamental_data(ticker)
            if data:
                # Displaying the fundamental analysis data
                st.subheader(f"Fundamental Analysis for {ticker}")
                st.json(data)  # Display data as JSON for simplicity
            else:
                st.error("Failed to fetch or display fundamental data.")

if __name__ == "__main__":
    app()
