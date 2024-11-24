import streamlit as st
import requests

# Set the backend URL where the analysis data is fetched
BACKEND_URL = "http://localhost:8000"

def fetch_overview_data(ticker):
    """Fetches stock overview data from the backend."""
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type=overview")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch overview data for {ticker}: HTTP Status Code {response.status_code}")
        return None

def app():
    """Main function for the Streamlit application."""
    st.set_page_config(page_title="Stock Overview", layout="wide")
    st.title('Stock Overview')

    ticker = st.text_input('Enter the stock ticker (e.g., AAPL):', '')

    if ticker:
        if st.button('Show Overview'):
            data = fetch_overview_data(ticker)
            if data:
                # Displaying the overview data
                st.subheader(f"Overview for {ticker}")
                st.write(f"**Price:** ${data.get('price', 'N/A')}")
                st.write(f"**Market Cap:** {data.get('market_cap', 'N/A')}")
                st.write(f"**P/E Ratio:** {data.get('pe_ratio', 'N/A')}")
                st.write(f"**Dividend Yield:** {data.get('dividend_yield', 'N/A')}%")
            else:
                st.error("Failed to fetch or display overview data.")

if __name__ == "__main__":
    app()
