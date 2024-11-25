import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

# Configure page settings
st.set_page_config(
    page_title="Advanced Technical Analysis Dashboard",
    page_icon="📊",
    layout="wide",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 0 1rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .filter-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

class EnhancedTechnicalAnalysis:
    def __init__(self):
        self.BACKEND_URL = "http://localhost:8000"
        self.indicators_map = {
            "Moving Averages": ["SMA 50", "SMA 200", "EMA 12", "EMA 26"],
            "Oscillators": ["RSI", "MACD Line", "Signal Line", "Stochastic K", "Stochastic D"],
            "Trend Indicators": ["Parabolic SAR"],
            "Volatility Indicators": ["Bollinger Bands", "ATR"],
            "Volume Indicators": ["OBV", "CMF"],
            "Support and Resistance": ["Support", "Resistance"]
        }
        
        self.time_ranges = {
            "1D": 1,
            "1W": 7,
            "1M": 30,
            "3M": 90,
            "6M": 180,
            "1Y": 365,
            "YTD": (datetime.now() - datetime(datetime.now().year, 1, 1)).days
        }

    def fetch_data(self, ticker: str, time_range: str) -> Dict:
        """Fetches technical analysis data with time range parameter."""
        try:
            days = self.time_ranges[time_range]
            response = requests.get(
                f"{self.BACKEND_URL}/analyze/{ticker}",
                params={
                    "analysis_type": "technical",
                    "days": days
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
            return None

    def create_advanced_chart(self, data: Dict, selected_category: str, selected_indicators: List[str], tickers: List[str]) -> go.Figure:
        """Creates an advanced interactive chart based on selected indicators."""
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.5, 0.25, 0.25],
            subplot_titles=('Technical Indicators', 'Volume', 'Oscillators')
        )

        for ticker in tickers:
            ticker_data = data.get(ticker)
            if not ticker_data:
                continue

            tech_data = ticker_data.get('Technical Analysis', {})
            
            # Plot selected indicators based on category
            if selected_category in tech_data:
                category_data = tech_data[selected_category]
                
                for indicator in selected_indicators:
                    indicator_key = indicator.replace(' ', '_')
                    if indicator_key in category_data:
                        indicator_data = category_data[indicator_key]
                        
                        # Determine which subplot to use
                        row = 1  # Default to main chart
                        if selected_category == "Volume Indicators":
                            row = 2
                        elif selected_category == "Oscillators":
                            row = 3
                            
                        fig.add_trace(
                            go.Scatter(
                                y=indicator_data,
                                name=f"{ticker} {indicator}",
                                mode='lines'
                            ),
                            row=row, col=1
                        )

                        # Add reference lines for specific indicators
                        if indicator == "RSI":
                            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
                            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
                        elif indicator == "Bollinger Bands":
                            # Add upper and lower bands
                            if "Upper_Band" in category_data and "Lower_Band" in category_data:
                                fig.add_trace(
                                    go.Scatter(
                                        y=category_data["Upper_Band"],
                                        name=f"{ticker} Upper Band",
                                        line=dict(dash='dash')
                                    ),
                                    row=1, col=1
                                )
                                fig.add_trace(
                                    go.Scatter(
                                        y=category_data["Lower_Band"],
                                        name=f"{ticker} Lower Band",
                                        line=dict(dash='dash')
                                    ),
                                    row=1, col=1
                                )

        # Update layout
        fig.update_layout(
            height=800,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor="rgba(255, 255, 255, 0.1)"
            ),
            margin=dict(l=50, r=50, t=50, b=50)
        )

        fig.update_xaxes(rangeslider_visible=True, row=3, col=1)
        
        return fig

def main():
    st.title("📈 Advanced Technical Analysis Dashboard")
    
    # Create filter container
    st.markdown("### 📊 Configuration")
    with st.container():
        # First row of filters
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            main_ticker = st.text_input("Primary Ticker:", placeholder="e.g., AAPL")
        
        with col2:
            compare_ticker = st.text_input("Comparison Ticker:", placeholder="e.g., MSFT")
            
        with col3:
            time_range = st.selectbox(
                "Time Range",
                ["1D", "1W", "1M", "3M", "6M", "1Y", "YTD"],
                index=3
            )
        
        # Second row of filters
        col1, col2 = st.columns([1, 2])
        
        analysis = EnhancedTechnicalAnalysis()
        
        with col1:
            indicator_category = st.selectbox(
                "Select Indicator Category:",
                list(analysis.indicators_map.keys())
            )
        
        with col2:
            selected_indicators = st.multiselect(
                "Select Indicators:",
                analysis.indicators_map[indicator_category],
                default=[analysis.indicators_map[indicator_category][0]]
            )

    # Analysis button
    if st.button("🔄 Generate Analysis", use_container_width=True):
        if main_ticker:
            with st.spinner("Fetching market data..."):
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📊 Charts", "📑 Analysis", "💡 Signals"])
                
                # Fetch data
                data = {}
                tickers = [main_ticker]
                main_data = analysis.fetch_data(main_ticker, time_range)
                
                if main_data:
                    data[main_ticker] = main_data
                    if compare_ticker:
                        compare_data = analysis.fetch_data(compare_ticker, time_range)
                        if compare_data:
                            data[compare_ticker] = compare_data
                            tickers.append(compare_ticker)
                    
                    # Tab 1: Charts
                    with tab1:
                        fig = analysis.create_advanced_chart(
                            data, 
                            indicator_category, 
                            selected_indicators, 
                            tickers
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Add your existing analysis and signals tabs implementation here
                    # [Previous implementation of tab2 and tab3 remains the same]
                
                else:
                    st.error("Failed to fetch data. Please check the ticker symbol and try again.")
        else:
            st.warning("Please enter at least one ticker symbol.")

if __name__ == "__main__":
    main()