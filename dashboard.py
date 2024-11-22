import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from utils.config import OPENAI_API_KEY
import openai

# Constants
BACKEND_URL = "http://localhost:8000"  # Adjust if hosted differently

def main():
    st.title('Multi-Agent Investment Analyst System')

    # Inputs for user interaction
    ticker1 = st.text_input('Enter the first stock ticker (e.g., AAPL):', key='ticker1')
    ticker2 = st.text_input('Enter the second stock ticker (e.g., MSFT):', key='ticker2')
    analysis_type = st.selectbox('Select the type of analysis:', ['fundamental', 'technical', 'both'])
    submit = st.button('Analyze and Compare')

    if submit and ticker1 and ticker2 and analysis_type:
        # Fetch analysis from the backend for both tickers
        data1 = fetch_data(ticker1, analysis_type)
        data2 = fetch_data(ticker2, analysis_type)

        if data1 and data2:
            display_comparative_results(data1, data2, analysis_type)
        else:
            st.error("Failed to fetch data for one or both tickers. Please check the tickers and try again.")

def fetch_data(ticker, analysis_type):
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type={analysis_type}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_comparative_results(data1, data2, analysis_type):
    if analysis_type in ['fundamental', 'both']:
        st.header("Comparative Fundamental Analysis")
        compare_fundamental(data1['Fundamental Analysis'], data2['Fundamental Analysis'])

    if analysis_type in ['technical', 'both']:
        st.header("Comparative Technical Analysis")
        compare_technical(data1['Technical Analysis'], data2['Technical Analysis'])

def compare_fundamental(fa1, fa2):
    df1 = pd.DataFrame(list(fa1['ratios'].items()), columns=['Ratio', 'Value1'])
    df2 = pd.DataFrame(list(fa2['ratios'].items()), columns=['Ratio', 'Value2'])
    df = pd.merge(df1, df2, on='Ratio')
    fig = px.bar(df, x='Ratio', y=['Value1', 'Value2'], barmode='group', title='Key Financial Ratios Comparison')
    st.plotly_chart(fig)

def compare_technical(ta1, ta2):
    # Assuming SMA is present for simplicity, expand as needed
    df1 = pd.DataFrame(ta1['SMA'], columns=['SMA1'])
    df2 = pd.DataFrame(ta2['SMA'], columns=['SMA2'])
    df1['Index'] = df1.index
    df2['Index'] = df2.index
    df = pd.merge(df1, df2, on='Index')
    fig = px.line(df, x='Index', y=['SMA1', 'SMA2'], title='SMA Comparison')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
