import streamlit as st
import requests

# Set the backend URL where the analysis data is fetched
BACKEND_URL = "http://localhost:8000"

def fetch_technical_data(ticker):
    """Fetches technical analysis data from the backend."""
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type=technical")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch technical data for {ticker}: HTTP Status Code {response.status_code}")
        return None

def app():
    """Main function for the Streamlit application."""
    st.set_page_config(page_title="Technical Analysis", layout="wide")
    st.title('Technical Analysis')

    ticker = st.text_input('Enter the stock ticker for technical analysis (e.g., GOOGL):', '')

    if ticker:
        if st.button('Analyze Technicals'):
            data = fetch_technical_data(ticker)
            if data:
                # Displaying the technical analysis data
                st.subheader(f"Technical Analysis for {ticker}")
                st.json(data)  # Display data as JSON for simplicity
            else:
                st.error("Failed to fetch or display technical data.")

if __name__ == "__main__":
    app()
