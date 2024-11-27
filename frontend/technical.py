import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime

class TechnicalAnalysisDashboard:
    def __init__(self):
        """
        Initialize Technical Analysis Dashboard with configurations and color schemes.
        Sets up the page layout and defines available indicators.
        """
        # Backend API configuration
        self.BACKEND_URL = "http://localhost:8000"
        
        # Initialize page configuration
        self.setup_page_config()
        
        # Define color scheme for consistent styling
        self.colors = {
            'primary': '#1e3c72',      # Main brand color
            'secondary': '#2a5298',     # Secondary brand color
            'success': '#10B981',       # Positive indicators
            'danger': '#EF4444',        # Negative indicators
            'warning': '#F59E0B',       # Warning indicators
            'info': '#3B82F6',          # Informational elements
            'background': '#f5f7fa',    # Background color
            'card': '#ffffff',          # Card background
            'text': '#1a1a1a'           # Text color
        }
        
        # Define available technical indicators and their categories
        self.indicators_map = {
            "Moving Averages": {
                "Trend Following": ["SMA 50", "SMA 200", "EMA 12", "EMA 26"],
                "Price Action": ["Price", "Volume"]
            },
            "Momentum Indicators": {
                "Oscillators": ["RSI", "Stochastic K", "Stochastic D"],
                "MACD": ["MACD Line", "Signal Line", "MACD Histogram"]
            },
            "Volatility Indicators": {
                "Bands": ["Bollinger Bands"],
                "Other": ["ATR", "Standard Deviation"]
            },
            "Volume Indicators": {
                "Volume Analysis": ["OBV", "CMF"],
                "Price-Volume": ["Volume by Price", "VWAP"]
            }
        }
        
        # Color mapping for specific indicators
        self.indicator_colors = {
            "SMA 50": self.colors['primary'],
            "SMA 200": self.colors['secondary'],
            "EMA 12": self.colors['info'],
            "EMA 26": self.colors['warning'],
            "RSI": "purple",
            "MACD Line": self.colors['primary'],
            "Signal Line": self.colors['warning'],
            "MACD Histogram": self.colors['info'],
            "Bollinger Bands": self.colors['primary'],
            "Volume": self.colors['success']
        }

    def setup_page_config(self):
        """Configure Streamlit page settings and apply custom styling"""
        st.set_page_config(
            page_title="Technical Analysis Pro",
            page_icon="📈",
            layout="wide"
        )
        st.markdown(self._get_custom_css(), unsafe_allow_html=True)

    def _get_custom_css(self) -> str:
        """
        Define custom CSS styling for the dashboard.
        Returns:
            str: CSS styling string
        """
        return """
        <style>
            /* Main Container Styling */
            .main {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 1rem;
            }
            
            /* Header Styling */
            .header-container {
                background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                margin-bottom: 2rem;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            /* Controls Container */
            .controls-container {
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            
            /* Chart Container */
            .chart-container {
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            
            .chart-container:hover {
                transform: translateY(-5px);
            }
            
            /* Indicator Selection */
            .indicator-category {
                background: white;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                border-left: 4px solid #1e3c72;
            }
            
            /* Button Styling */
            .stButton > button {
                background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            
            /* Input Fields */
            .stTextInput > div > div {
                background: white;
                border-radius: 8px;
                border: 2px solid #e2e8f0;
                transition: all 0.3s ease;
            }
            
            .stTextInput > div > div:focus-within {
                border-color: #1e3c72;
                box-shadow: 0 0 0 2px rgba(30,60,114,0.2);
            }
            
            /* Metrics Display */
            .metric-container {
                background: white;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                border-left: 4px solid #1e3c72;
                transition: transform 0.3s ease;
            }
            
            .metric-container:hover {
                transform: translateX(5px);
            }
            
            /* Loading Animation */
            .loading-spinner {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 2rem;
            }
            
            /* Indicator Values */
            .indicator-value {
                font-size: 1.25rem;
                font-weight: bold;
                margin: 0.5rem 0;
            }
            
            .value-positive {
                color: #10B981;
            }
            
            .value-negative {
                color: #EF4444;
            }
            
            /* Category Headers */
            .category-header {
                background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 1rem;
                border-radius: 10px;
                margin: 1rem 0;
            }
        </style>
        """

    def fetch_data(self, ticker: str) -> Dict:
        """
        Fetch technical analysis data from backend API.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            Dict: Technical analysis data or None if fetch fails
        """
        try:
            response = requests.get(
                f"{self.BACKEND_URL}/analyze/{ticker}",
                params={"analysis_type": "technical"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
            return None


    def create_indicator_chart(self, data_dict: Dict, indicator: str, comparison_data: Dict = None) -> go.Figure:
        """
        Create interactive chart for technical indicators with improved labeling and combined comparison.
        
        Args:
            data_dict (Dict): Primary stock's technical analysis data
            indicator (str): Indicator name to plot
            comparison_data (Dict): Optional comparison stock's data
            
        Returns:
            go.Figure: Plotly figure with combined data
        """
        try:
            fig = go.Figure()
            tech_data = data_dict.get('Technical Analysis', {})
            dates = list(range(len(next(iter(next(iter(tech_data.values())).values())))))

            def add_indicator_trace(data, ticker_name, line_style=None):
                """Helper function to add indicator traces"""
                if indicator in ["SMA 50", "SMA 200", "EMA 12", "EMA 26"]:
                    indicator_key = indicator.replace(' ', '_')
                    if 'Moving Averages' in data and indicator_key in data['Moving Averages']:
                        indicator_data = data['Moving Averages'][indicator_key]
                        fig.add_trace(
                            go.Scatter(
                                x=dates,
                                y=indicator_data,
                                name=f"{indicator} ({ticker_name})",
                                line=line_style or dict(
                                    color=self.indicator_colors.get(indicator, self.colors['primary']),
                                    width=2
                                )
                            )
                        )
                
                elif indicator == "RSI":
                    if 'Oscillators' in data and 'RSI' in data['Oscillators']:
                        rsi_data = data['Oscillators']['RSI']
                        fig.add_trace(
                            go.Scatter(
                                x=dates,
                                y=rsi_data,
                                name=f"RSI ({ticker_name})",
                                line=line_style or dict(color='purple', width=2)
                            )
                        )
                
                elif indicator in ["MACD Line", "Signal Line"]:
                    if 'Oscillators' in data and 'MACD' in data['Oscillators']:
                        macd_key = 'MACD_Line' if indicator == "MACD Line" else "Signal_Line"
                        macd_data = data['Oscillators']['MACD'][macd_key]
                        fig.add_trace(
                            go.Scatter(
                                x=dates,
                                y=macd_data,
                                name=f"{indicator} ({ticker_name})",
                                line=line_style or dict(
                                    color=self.indicator_colors.get(indicator, self.colors['primary']),
                                    width=2
                                )
                            )
                        )
                
                elif indicator == "Bollinger Bands":
                    if 'Volatility Indicators' in data and 'Bollinger_Bands' in data['Volatility Indicators']:
                        bb_data = data['Volatility Indicators']['Bollinger_Bands']
                        color = self.colors['primary'] if not line_style else self.colors['secondary']
                        
                        fig.add_trace(
                            go.Scatter(
                                x=dates,
                                y=bb_data['Upper'],
                                name=f'Upper Band ({ticker_name})',
                                line=dict(color=color, dash='dash', width=1)
                            )
                        )
                        fig.add_trace(
                            go.Scatter(
                                x=dates,
                                y=bb_data['Lower'],
                                name=f'Lower Band ({ticker_name})',
                                line=dict(color=color, dash='dash', width=1),
                                fill='tonexty',
                                fillcolor=f'rgba{tuple(list(self.hex_to_rgb(color)) + [0.1])}'
                            )
                        )

            # Add primary stock data
            add_indicator_trace(tech_data, "Primary")

            # Add comparison data if provided
            if comparison_data:
                comp_tech_data = comparison_data.get('Technical Analysis', {})
                add_indicator_trace(
                    comp_tech_data, 
                    "Comparison",
                    line_style=dict(
                        color=self.colors['secondary'],
                        width=2,
                        dash='solid'
                    )
                )

            # Add indicator-specific reference lines
            if indicator == "RSI":
                fig.add_hline(
                    y=70, 
                    line_dash="dash", 
                    line_color=self.colors['danger'],
                    annotation_text="Overbought",
                    annotation_position="right"
                )
                fig.add_hline(
                    y=30, 
                    line_dash="dash", 
                    line_color=self.colors['success'],
                    annotation_text="Oversold",
                    annotation_position="right"
                )

            # Enhanced chart layout
            fig.update_layout(
                title=dict(
                    text=f"{indicator} Analysis",
                    x=0.5,
                    xanchor='center',
                    font=dict(size=20)
                ),
                height=500,
                showlegend=True,
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor=self.colors['primary'],
                    borderwidth=1
                ),
                margin=dict(l=60, r=40, t=80, b=60)
            )

            # Enhanced axes labels
            y_axis_labels = {
                "RSI": "RSI Value (0-100)",
                "MACD Line": "MACD Value",
                "Signal Line": "Signal Value",
                "Bollinger Bands": "Price",
                "SMA 50": "Moving Average Value",
                "SMA 200": "Moving Average Value",
                "EMA 12": "Moving Average Value",
                "EMA 26": "Moving Average Value"
            }

            fig.update_xaxes(
                title="Trading Days",
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(0,0,0,0.1)',
                zeroline=False,
                showticklabels=True,
                tickmode='linear',
                tick0=0,
                dtick=5
            )
            
            fig.update_yaxes(
                title=y_axis_labels.get(indicator, indicator),
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(0,0,0,0.1)',
                zeroline=False
            )

            return fig

        except Exception as e:
            st.error(f"Error creating chart for {indicator}: {str(e)}")
            return None


    def display_indicator_metrics(self, data: Dict, indicator: str):
        """
        Display current metrics and trends for an indicator.
        
        Args:
            data (Dict): Technical analysis data
            indicator (str): Name of the indicator
        """
        try:
            tech_data = data.get('Technical Analysis', {})
            current_value = None
            prev_value = None

            # Extract values based on indicator type
            if indicator in ["SMA 50", "SMA 200", "EMA 12", "EMA 26"]:
                indicator_key = indicator.replace(' ', '_')
                values = tech_data.get('Moving Averages', {}).get(indicator_key, [])
                if values:
                    current_value = values[-1]
                    prev_value = values[-2] if len(values) > 1 else current_value
            
            elif indicator == "RSI":
                values = tech_data.get('Oscillators', {}).get('RSI', [])
                if values:
                    current_value = values[-1]
                    prev_value = values[-2] if len(values) > 1 else current_value
            
            elif indicator in ["MACD Line", "Signal Line"]:
                macd_key = 'MACD_Line' if indicator == "MACD Line" else "Signal_Line"
                values = tech_data.get('Oscillators', {}).get('MACD', {}).get(macd_key, [])
                if values:
                    current_value = values[-1]
                    prev_value = values[-2] if len(values) > 1 else current_value

            # Display metrics if available
            if current_value is not None and prev_value is not None:
                change = current_value - prev_value
                trend_class = "value-positive" if change >= 0 else "value-negative"
                
                st.markdown(f"""
                <div class="metric-container">
                    <h4>{indicator}</h4>
                    <div class="indicator-value {trend_class}">
                        {current_value:.2f}
                        <span style="font-size: 0.8em;">
                            ({'+' if change >= 0 else ''}{change:.2f})
                        </span>
                    </div>
                    <div style="font-size: 0.9em; color: #666;">
                        Trend: {"Upward" if change >= 0 else "Downward"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            print(f"Error displaying metrics for {indicator}: {str(e)}")

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to RGB values.
        
        Args:
            hex_color (str): Hex color code
            
        Returns:
            Tuple[int, int, int]: RGB values
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def run(self):
        """
        Main dashboard execution method with improved comparison handling
        and unique chart identifiers.
        """
        # Display header
        st.markdown("""
        <div class="header-container">
            <h1 style="font-size: 3rem;">📈 Technical Analysis Pro</h1>
            <p style="font-size: 1.2rem;">Advanced Technical Indicators & Analysis</p>
        </div>
        """, unsafe_allow_html=True)

        # Configuration section
        st.markdown('<div class="controls-container">', unsafe_allow_html=True)
        
        # Input fields
        col1, col2 = st.columns([1, 1])
        with col1:
            ticker = st.text_input("Primary Ticker:", placeholder="e.g., AAPL").upper()
        with col2:
            compare_ticker = st.text_input("Comparison Ticker:", placeholder="e.g., MSFT").upper()

        # Indicator selection organized by categories
        selected_indicators = []
        for category, subcategories in self.indicators_map.items():
            st.markdown(f"""
            <div class="category-header">
                <h3>{category}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            cols = st.columns(len(subcategories))
            for col, (subcat, indicators) in zip(cols, subcategories.items()):
                with col:
                    st.markdown(f"<h4>{subcat}</h4>", unsafe_allow_html=True)
                    for ind in indicators:
                        if st.checkbox(ind, key=f"check_{category}_{ind}"):
                            selected_indicators.append(ind)

        st.markdown('</div>', unsafe_allow_html=True)

        # Analysis section
        if st.button("🔄 Generate Analysis", use_container_width=True):
            if ticker:
                with st.spinner(f"Analyzing {ticker}..."):
                    # Fetch data for primary ticker
                    primary_data = self.fetch_data(ticker)
                    compare_data = None
                    
                    # Fetch comparison data if provided
                    if compare_ticker:
                        with st.spinner(f"Fetching comparison data for {compare_ticker}..."):
                            compare_data = self.fetch_data(compare_ticker)
                    
                    if primary_data:
                        # Display selected indicators
                        for idx, indicator in enumerate(selected_indicators):
                            st.markdown(f'<div class="chart-container">', unsafe_allow_html=True)
                            
                            # Create columns for chart and metrics
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                # Create chart with comparison data if available
                                chart = self.create_indicator_chart(
                                    primary_data, 
                                    indicator,
                                    compare_data if compare_ticker else None
                                )
                                
                                if chart:
                                    # Use unique key for each chart
                                    st.plotly_chart(
                                        chart, 
                                        use_container_width=True,
                                        key=f"chart_{indicator}_{idx}"
                                    )
                            
                            with col2:
                                # Display metrics for both tickers
                                st.markdown("### Primary Metrics")
                                self.display_indicator_metrics(primary_data, indicator)
                                
                                if compare_data:
                                    st.markdown("### Comparison Metrics")
                                    self.display_indicator_metrics(compare_data, indicator)
                            
                            st.markdown('</div>', unsafe_allow_html=True)

                            # Add analysis summary if available
                            if self.get_indicator_analysis(primary_data, indicator):
                                st.markdown("""
                                <div class="analysis-container">
                                    <h4>Analysis Summary</h4>
                                """, unsafe_allow_html=True)
                                
                                analysis = self.get_indicator_analysis(primary_data, indicator)
                                st.markdown(f"<p>{analysis}</p>", unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)

                    else:
                        st.error(f"Failed to fetch data for {ticker}. Please check the ticker symbol.")
            else:
                st.warning("Please enter at least one ticker symbol.")

    def get_indicator_analysis(self, data: dict, indicator: str) -> str:
        """
        Generate analysis summary for the indicator.
        
        Args:
            data (dict): Technical analysis data
            indicator (str): Indicator name
            
        Returns:
            str: Analysis summary or None if not available
        """
        try:
            tech_data = data.get('Technical Analysis', {})
            
            if indicator == "RSI":
                rsi_values = tech_data.get('Oscillators', {}).get('RSI', [])
                if rsi_values:
                    current_rsi = rsi_values[-1]
                    if current_rsi > 70:
                        return "RSI indicates overbought conditions. Consider potential reversal."
                    elif current_rsi < 30:
                        return "RSI indicates oversold conditions. Watch for possible bounce."
                    else:
                        return "RSI is in neutral territory."
            
            elif "SMA" in indicator or "EMA" in indicator:
                ma_values = tech_data.get('Moving Averages', {}).get(indicator.replace(' ', '_'), [])
                if ma_values and len(ma_values) > 1:
                    current = ma_values[-1]
                    previous = ma_values[-2]
                    trend = "upward" if current > previous else "downward"
                    return f"{indicator} shows {trend} trend momentum."
            
            elif "MACD" in indicator:
                macd_data = tech_data.get('Oscillators', {}).get('MACD', {})
                if macd_data:
                    macd_line = macd_data.get('MACD_Line', [])
                    signal_line = macd_data.get('Signal_Line', [])
                    if macd_line and signal_line:
                        current_macd = macd_line[-1]
                        current_signal = signal_line[-1]
                        if current_macd > current_signal:
                            return "MACD is above signal line, indicating bullish momentum."
                        else:
                            return "MACD is below signal line, indicating bearish momentum."

            return None

        except Exception as e:
            print(f"Error generating analysis for {indicator}: {str(e)}")
            return None

if __name__ == "__main__":
    dashboard = TechnicalAnalysisDashboard()
    dashboard.run()
