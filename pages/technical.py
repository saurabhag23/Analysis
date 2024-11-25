import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Tuple

BACKEND_URL = "http://localhost:8000"

class TechnicalAnalysisComparison:
    def __init__(self):
        self.indicators_map = {
            "Moving Averages": ["SMA 50", "SMA 200", "EMA 12", "EMA 26"],
            "Oscillators": ["RSI", "MACD Line", "Signal Line", "Stochastic K", "Stochastic D"],
            "Trend Indicators": ["Parabolic SAR"],
            "Volatility Indicators": ["Bollinger Bands", "ATR"],
            "Volume Indicators": ["OBV", "CMF"],
            "Support and Resistance": ["Support", "Resistance"],
            "Additional Indicators": ["CCI", "ROC", "PVT", "ADL"]
        }
        
    def fetch_technical_data(self, ticker: str) -> Dict:
        """Fetches technical analysis data from the backend."""
        response = requests.get(f"{BACKEND_URL}/analyze/{ticker}?analysis_type=technical")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch technical data for {ticker}: HTTP Status Code {response.status_code}")
            return None

    def create_plot(self, data: Dict, indicator: str, tickers: List[str]) -> go.Figure:
        """Creates a plot for the selected indicator and tickers."""
        fig = go.Figure()
        
        for ticker in tickers:
            ticker_data = data.get(ticker)
            if not ticker_data:
                continue
                
            values = self._get_indicator_values(ticker_data, indicator)
            if values:
                x_range = list(range(len(values)))
                fig.add_trace(go.Scatter(
                    x=x_range,
                    y=values,
                    mode='lines',
                    name=f'{ticker} - {indicator}'
                ))

        # Add indicator-specific layout elements
        if indicator == "RSI":
            fig.add_hline(y=70, line_color='red', line_dash='dash', annotation_text="Overbought")
            fig.add_hline(y=30, line_color='green', line_dash='dash', annotation_text="Oversold")
        elif indicator == "Bollinger Bands":
            # Add both upper and lower bands
            for ticker in tickers:
                ticker_data = data.get(ticker)
                if ticker_data:
                    upper = self._get_indicator_values(ticker_data, "Upper Band")
                    lower = self._get_indicator_values(ticker_data, "Lower Band")
                    if upper and lower:
                        x_range = list(range(len(upper)))
                        fig.add_trace(go.Scatter(x=x_range, y=upper, mode='lines', name=f'{ticker} - Upper Band'))
                        fig.add_trace(go.Scatter(x=x_range, y=lower, mode='lines', name=f'{ticker} - Lower Band'))

        fig.update_layout(
            title=f'{indicator} Comparison',
            xaxis_title='Days',
            yaxis_title=indicator,
            plot_bgcolor='rgba(240, 240, 240, 0.8)',
            showlegend=True
        )
        
        return fig

    def _get_indicator_values(self, data: Dict, indicator: str) -> List[float]:
        """Retrieves the values for a specific indicator from the data."""
        if indicator in ["SMA 50", "SMA 200", "EMA 12", "EMA 26"]:
            return data['Technical Analysis']['Moving Averages'].get(f"{indicator.replace(' ', '_')}", [])
        elif indicator in ["RSI"]:
            return data['Technical Analysis']['Oscillators'].get(indicator, [])
        elif indicator in ["MACD Line", "Signal Line"]:
            return data['Technical Analysis']['Oscillators']['MACD'].get(f"{indicator.replace(' ', '_')}", [])
        elif indicator in ["Stochastic K", "Stochastic D"]:
            return data['Technical Analysis']['Oscillators']['Stochastic'].get(indicator[-1], [])
        elif indicator == "Parabolic SAR":
            return data['Technical Analysis']['Trend Indicators'].get('Parabolic_SAR', [])
        elif indicator == "ATR":
            return data['Technical Analysis']['Volatility Indicators'].get(indicator, [])
        elif indicator in ["OBV", "CMF"]:
            return data['Technical Analysis']['Volume Indicators'].get(indicator, [])
        elif indicator in ["Support", "Resistance"]:
            return data['Technical Analysis']['Support and Resistance'].get(indicator.lower(), [])
        elif indicator in ["CCI", "ROC", "PVT", "ADL"]:
            return data['Technical Analysis']['Additional Indicators'].get(indicator, [])
        return []

def app():
    """Main function for the Streamlit application."""
    st.set_page_config(page_title="Technical Analysis Comparison", layout="wide")
    
    # Initialize the analysis class
    analysis = TechnicalAnalysisComparison()
    
    st.title('Technical Analysis Comparison Dashboard')
    
    # Create columns for input fields
    col1, col2 = st.columns([2, 1])
    
    # Main ticker input
    with col1:
        main_ticker = st.text_input('Enter the main stock ticker (e.g., AAPL):', '')
    
    # Comparison ticker input
    with col2:
        compare_ticker = st.text_input('Enter ticker to compare (optional):', '')
    
    # Create indicator selection dropdown
    indicator_category = st.selectbox(
        'Select Indicator Category:',
        list(analysis.indicators_map.keys())
    )
    
    specific_indicator = st.selectbox(
        'Select Specific Indicator:',
        analysis.indicators_map[indicator_category]
    )
    
    if main_ticker:
        if st.button('Generate Analysis'):
            # Fetch data for both tickers
            data = {}
            tickers = [main_ticker]
            
            main_data = analysis.fetch_technical_data(main_ticker)
            if main_data:
                data[main_ticker] = main_data
                
                if compare_ticker:
                    compare_data = analysis.fetch_technical_data(compare_ticker)
                    if compare_data:
                        data[compare_ticker] = compare_data
                        tickers.append(compare_ticker)
                
                # Create and display the selected plot
                fig = analysis.create_plot(data, specific_indicator, tickers)
                st.plotly_chart(fig, use_container_width=True)
                
                # Add analysis summary
                st.subheader("Analysis Summary")
                for ticker in tickers:
                    st.write(f"**{ticker}** Analysis:")
                    # Add your analysis logic here based on the indicator values
                    st.write("- Indicator values and interpretations would go here")
                    st.write("- Trading signals and recommendations would go here")
            else:
                st.error("Failed to fetch technical data.")

if __name__ == "__main__":
    app()