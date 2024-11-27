import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from typing import Dict, List
import requests
import json
from streamlit_lottie import st_lottie
class FundamentalAnalysisDashboard:
    def __init__(self):
        self.BACKEND_URL = "http://localhost:8000"
        self.initialize_session_state()
        self.setup_page_config()
        self.colors = {
            'primary': '#1e3c72',
            'secondary': '#2a5298',
            'success': '#10B981',
            'danger': '#EF4444',
            'warning': '#F59E0B',
            'background': '#f5f7fa',
            'text': '#1a1a1a'
        }
        self.load_animations()
    def load_animations(self):
        def load_lottieurl(url: str):
            try:
                r = requests.get(url)
                if r.status_code != 200:
                    return None
                return r.json()
            except:
                return None

        self.lottie_chart = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json")
        
    def display_animations(self):
        
        if self.lottie_chart:
            st_lottie(self.lottie_chart, height=200, key="chart")
        else:
            st.warning("Chart animation could not be loaded.")
        

    def _get_custom_css(self) -> str:
        return """
        <style>
        /* Existing styles */

        /* New styles */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }

        .widget-container {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            backdrop-filter: blur(5px);
        }

        .stButton > button {
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }

        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }

        .chart-container {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .chart-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }
        </style>
        """

    
    def initialize_session_state(self):
        if 'analysis_data' not in st.session_state:
            st.session_state.analysis_data = {}
        if 'selected_stock' not in st.session_state:
            st.session_state.selected_stock = None
        if 'comparison_data' not in st.session_state:
            st.session_state.comparison_data = {}

    def setup_page_config(self):
        st.set_page_config(
            page_title="Fundamental Analysis Pro",
            page_icon="📊",
            layout="wide"
        )
        st.markdown(self._get_custom_css(), unsafe_allow_html=True)

    def _get_custom_css(self) -> str:
        return """
        <style>
        /* ... (keep your existing CSS) ... */
        </style>
        """

    def fetch_fundamental_data(self, ticker: str) -> Dict:
        try:
            response = requests.get(
                f"{self.BACKEND_URL}/analyze/{ticker}?analysis_type=fundamental",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            st.error(f"Failed to fetch data for {ticker}: {response.status_code}")
            return None
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return None

    def create_bar_chart(self, ratios: Dict, ticker: str, compare_ratios: Dict = None, compare_ticker: str = None) -> go.Figure:
        metrics = ['ROE', 'ROA', 'Profit Margin', 'Operating Margin', 'Asset Turnover']
        values = [ratios.get(metric, 0) * 100 for metric in metrics]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=metrics,
            y=values,
            name=ticker,
            marker_color=self.colors['primary']
        ))
        
        if compare_ratios and compare_ticker:
            compare_values = [compare_ratios.get(metric, 0) * 100 for metric in metrics]
            fig.add_trace(go.Bar(
                x=metrics,
                y=compare_values,
                name=compare_ticker,
                marker_color=self.colors['secondary']
            ))
        
        fig.update_layout(
            title='Financial Performance Comparison',
            xaxis_title='Metrics',
            yaxis_title='Percentage (%)',
            barmode='group',
            height=500
        )
        
        return fig

    def create_growth_chart(self, ratios: Dict, ticker: str, compare_ratios: Dict = None, compare_ticker: str = None) -> go.Figure:
        growth_metrics = ['Revenue Growth Rate', 'Net Income Growth Rate']
        fig = go.Figure()
        
        values = [ratios.get(metric, 0) * 100 for metric in growth_metrics]
        fig.add_trace(go.Bar(
            x=growth_metrics,
            y=values,
            name=ticker,
            marker_color=self.colors['primary']
        ))
        
        if compare_ratios and compare_ticker:
            compare_values = [compare_ratios.get(metric, 0) * 100 for metric in growth_metrics]
            fig.add_trace(go.Bar(
                x=growth_metrics,
                y=compare_values,
                name=compare_ticker,
                marker_color=self.colors['secondary']
            ))
        
        fig.update_layout(
            title='Growth Metrics Comparison',
            yaxis_title='Percentage (%)',
            barmode='group',
            height=400
        )
        
        return fig

    def display_key_metrics(self, ratios: Dict, ticker: str):
        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            ("ROE", ratios.get('ROE', 0) * 100, "%", col1),
            ("P/E Ratio", ratios.get('P/E Ratio', 0), "", col2),
            ("Profit Margin", ratios.get('Profit Margin', 0) * 100, "%", col3),
            ("Dividend Yield", ratios.get('Dividend Yield', 0) * 100, "%", col4)
        ]
        for metric, value, suffix, col in metrics:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{metric}</div>
                    <div class="metric-value">
                        {value:.2f}{suffix}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    def display_narrative(self, narrative: str):
        st.markdown("""
        <div class="narrative-container">
            <h3>📝 Analysis Narrative</h3>
        """, unsafe_allow_html=True)
        
        points = narrative.split('\n\n')
        for point in points:
            if point.strip():
                st.markdown(f"""
                <div class="narrative-point">
                    {point}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def create_individual_ratio_charts(self, ratios: Dict, ticker: str, compare_ratios: Dict = None, compare_ticker: str = None):
        metrics = ['ROE', 'ROA', 'Profit Margin', 'Operating Margin', 'Asset Turnover', 'P/E Ratio', 'Dividend Yield']
        
        for metric in metrics:
            fig = go.Figure()
            
            value = ratios.get(metric, 0)
            fig.add_trace(go.Bar(
                x=[ticker],
                y=[value],
                name=ticker,
                marker_color=self.colors['primary']
            ))
            
            if compare_ratios and compare_ticker:
                compare_value = compare_ratios.get(metric, 0)
                fig.add_trace(go.Bar(
                    x=[compare_ticker],
                    y=[compare_value],
                    name=compare_ticker,
                    marker_color=self.colors['secondary']
                ))
            
            fig.update_layout(
                title=f'{metric} Comparison',
                yaxis_title='Value',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)

    def run(self):
        st.markdown("""
        <div class="header-container">
            <h1 style="font-size: 3rem;">📊 Fundamental Analysis Pro</h1>
            <p style="font-size: 1.2rem;">Comprehensive Financial Analysis & Insights</p>
        </div>
        """, unsafe_allow_html=True)
        self.display_animations()
        with st.container():
            st.markdown('<div class="widget-container">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                ticker = st.text_input("Enter Stock Ticker:", placeholder="e.g., MSFT").upper()
            with col2:
                compare_ticker = st.text_input("Compare with:", placeholder="e.g., AAPL").upper()
            with col3:
                analyze = st.button("🔍 Analyze", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if analyze and ticker:
            with st.spinner(f"Analyzing {ticker}..."):
                data = self.fetch_fundamental_data(ticker)
            
            compare_data = None
            if compare_ticker:
                with st.spinner(f"Fetching comparison data for {compare_ticker}..."):
                    compare_data = self.fetch_fundamental_data(compare_ticker)

            if data:
                fundamental_data = data['Fundamental Analysis']
                ratios = fundamental_data['ratios']
                narrative = fundamental_data['narrative']

                # Display metrics for both tickers
                st.markdown("### Key Metrics")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"#### {ticker}")
                    self.display_key_metrics(ratios, ticker)
                with col2:
                    if compare_data:
                        st.markdown(f"#### {compare_ticker}")
                        compare_ratios = compare_data['Fundamental Analysis']['ratios']
                        self.display_key_metrics(compare_ratios, compare_ticker)

                # Charts section
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    bar_chart = self.create_bar_chart(
                        ratios, ticker,
                        compare_data['Fundamental Analysis']['ratios'] if compare_data else None,
                        compare_ticker if compare_data else None
                    )
                    st.plotly_chart(bar_chart, use_container_width=True)
                with col2:
                    growth_chart = self.create_growth_chart(
                        ratios, ticker,
                        compare_data['Fundamental Analysis']['ratios'] if compare_data else None,
                        compare_ticker if compare_data else None
                    )
                    st.plotly_chart(growth_chart, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Individual ratio charts
                st.markdown("### Individual Ratio Comparisons")
                self.create_individual_ratio_charts(
                    ratios, ticker,
                    compare_data['Fundamental Analysis']['ratios'] if compare_data else None,
                    compare_ticker if compare_data else None
                )

                # Narrative section
                self.display_narrative(narrative)

            else:
                st.error("Failed to fetch data. Please check the ticker symbol.")

if __name__ == "__main__":
    dashboard = FundamentalAnalysisDashboard()
    dashboard.run()