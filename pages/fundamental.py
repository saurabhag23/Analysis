import streamlit as st
import requests
import plotly.graph_objects as go

BACKEND_URL = "http://localhost:8000"

def fetch_fundamental_data(ticker):
    response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type=fundamental")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch fundamental data for {ticker}: HTTP Status Code {response.status_code}")
        return None

def plot_ratio(ratios, ratio_name, tickers):
    fig = go.Figure()
    for ticker in tickers:
        fig.add_trace(go.Bar(y=[ticker], x=[ratios[ticker][ratio_name]], name=ticker, orientation='h'))
    fig.update_layout(title=f'{ratio_name} Comparison', xaxis_title='Value', height=400)
    return fig

def plot_single_ratio(ratio_name, value, ticker):
    fig = go.Figure(go.Bar(y=[ratio_name], x=[value], orientation='h'))
    fig.update_layout(title=f'{ratio_name} for {ticker}', xaxis_title='Value', height=300)
    return fig

def app():
    st.set_page_config(page_title="Fundamental Analysis", layout="wide")
    st.title('Fundamental Analysis Dashboard')

    # Initialize session state variables
    if 'analysis_data' not in st.session_state:
        st.session_state.analysis_data = {}
    if 'comparisons' not in st.session_state:
        st.session_state.comparisons = []

    # Input for primary ticker
    ticker = st.text_input('Enter the stock ticker for fundamental analysis (e.g., MSFT):', '')

    if st.button('Analyze Fundamentals', key='analyze'):
        if ticker:
            data = fetch_fundamental_data(ticker)
            if data:
                st.session_state.analysis_data[ticker] = data['Fundamental Analysis']['ratios']

    # Display primary analysis results
    if st.session_state.analysis_data:
        for ticker, ratios in st.session_state.analysis_data.items():
            st.subheader(f"Fundamental Analysis for {ticker}")
            for ratio_name, value in ratios.items():
                st.plotly_chart(plot_single_ratio(ratio_name, value, ticker))

    # Input for comparison
    compare_ticker = st.text_input('Enter another ticker to compare:', '')

    if st.button('Compare', key='compare'):
        if compare_ticker:
            compare_data = fetch_fundamental_data(compare_ticker)
            if compare_data:
                st.session_state.comparisons.append({
                    'ticker': compare_ticker,
                    'ratios': compare_data['Fundamental Analysis']['ratios']
                })

    # Display comparison results
    if st.session_state.comparisons:
        for comparison in st.session_state.comparisons:
            compare_ticker = comparison['ticker']
            compare_ratios = comparison['ratios']
            st.subheader(f"Comparison with {compare_ticker}")
            tickers = list(st.session_state.analysis_data.keys()) + [compare_ticker]
            for ratio_name in st.session_state.analysis_data[tickers[0]].keys():
                all_ratios = {ticker: st.session_state.analysis_data[ticker] for ticker in st.session_state.analysis_data}
                all_ratios[compare_ticker] = compare_ratios
                st.plotly_chart(plot_ratio(all_ratios, ratio_name, tickers))

    # Input for third ticker comparison
    third_ticker = st.text_input('Enter a third ticker to compare (optional):', '')

    if st.button('Compare Three', key='compare_three'):
        if third_ticker:
            third_data = fetch_fundamental_data(third_ticker)
            if third_data:
                st.session_state.comparisons.append({
                    'ticker': third_ticker,
                    'ratios': third_data['Fundamental Analysis']['ratios']
                })

    # Display all comparisons
    if st.session_state.comparisons:
        tickers = list(st.session_state.analysis_data.keys()) + [comp['ticker'] for comp in st.session_state.comparisons]
        for ratio_name in st.session_state.analysis_data[tickers[0]].keys():
            all_ratios = {ticker: st.session_state.analysis_data[ticker] for ticker in st.session_state.analysis_data}
            for comp in st.session_state.comparisons:
                all_ratios[comp['ticker']] = comp['ratios']
            st.plotly_chart(plot_ratio(all_ratios, ratio_name, tickers))

if __name__ == "__main__":
    app()
