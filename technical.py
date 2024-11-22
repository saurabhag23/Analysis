import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Constants
BACKEND_URL = "http://localhost:8000"  # Adjust if hosted differently

def display_technical_analysis():
    st.header("Technical Analysis")

    # User input for stock ticker
    ticker = st.text_input('Enter the stock ticker (e.g., AAPL):')
    
    # Button to fetch and display data
    if st.button('Analyze Stock'):
        if ticker:
            data = fetch_technical_data(ticker)
            if data:
                display_technical_data(ticker, data)
            else:
                st.error(f"No technical data available for {ticker}.")

def fetch_technical_data(ticker):
    """Fetch technical data for a given ticker."""
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type=technical")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch technical data for {ticker}: HTTP Status Code {response.status_code}")
        return None

def display_technical_data(ticker, data):
    """Display technical data for the stock."""
    st.subheader(f"{ticker} Technical Indicators")

    # Display each technical indicator in a separate plot
    if 'SMA' in data:
        st.write("Simple Moving Averages")
        df_sma = pd.DataFrame(data['SMA'])
        st.plotly_chart(px.line(df_sma, x='Date', y='Value', title='SMA'))

    if 'EMA' in data:
        st.write("Exponential Moving Averages")
        df_ema = pd.DataFrame(data['EMA'])
        st.plotly_chart(px.line(df_ema, x='Date', y='Value', title='EMA'))

    if 'MACD' in data:
        st.write("MACD")
        df_macd = pd.DataFrame(data['MACD'])
        st.plotly_chart(px.line(df_macd, x='Date', y=['MACD', 'Signal'], title='MACD'))

    if 'RSI' in data:
        st.write("Relative Strength Index (RSI)")
        df_rsi = pd.DataFrame(data['RSI'])
        st.plotly_chart(px.line(df_rsi, x='Date', y='Value', title='RSI'))

if __name__ == "__main__":
    display_technical_analysis()
