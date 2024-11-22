import streamlit as st
import requests

# Constants
BACKEND_URL = "http://localhost:8000"  # Adjust if hosted differently

def main():
    st.title('Multi-Agent Investment Analyst System')

    # Inputs for user interaction
    ticker = st.text_input('Enter the stock ticker (e.g., AAPL, MSFT):')
    analysis_type = st.selectbox('Select the type of analysis:', ['fundamental', 'technical', 'both'])

    if ticker and analysis_type:
        # Fetch analysis from the backend
        response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type={analysis_type}")
        if response.status_code == 200:
            data = response.json()
            display_results(data, analysis_type)
        else:
            st.error("Failed to fetch data from backend. Please check the ticker and try again.")

def display_results(data, analysis_type):
    if 'Fundamental Analysis' in data and (analysis_type == 'fundamental' or analysis_type == 'both'):
        st.header("Fundamental Analysis")
        st.json(data['Fundamental Analysis'])

    if 'Technical Analysis' in data and (analysis_type == 'technical' or analysis_type == 'both'):
        st.header("Technical Analysis")
        technical_data = data['Technical Analysis']
        if 'SMA' in technical_data:
            st.subheader("Simple Moving Average (SMA)")
            st.line_chart(technical_data['SMA'])
        if 'EMA' in technical_data:
            st.subheader("Exponential Moving Average (EMA)")
            st.line_chart(technical_data['EMA'])
        # Add more plots for each technical indicator as needed

if __name__ == "__main__":
    main()
