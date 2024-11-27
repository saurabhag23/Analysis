import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import numpy as np
from cache_manager import RedisStockCache

class StockDashboard:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.cache = RedisStockCache()
        self.initialize_session_state()
        self.colors = {
            'primary': '#1e3c72',
            'secondary': '#2a5298',
            'success': '#10B981',
            'danger': '#EF4444',
            'background': '#f5f7fa',
            'card': '#ffffff',
            'text': '#1a1a1a'
        }
        self.setup_page_config()

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'analyzed_ticker' not in st.session_state:
            st.session_state.analyzed_ticker = None
        if 'selected_stock' not in st.session_state:
            st.session_state.selected_stock = None
        if 'defaults_loaded' not in st.session_state:
            st.session_state.defaults_loaded = False

    def setup_page_config(self):
        """Configure page settings and styling"""
        st.set_page_config(
            page_title="Stock Analysis Pro",
            page_icon="📈",
            layout="wide"
        )
        st.markdown(self._get_custom_css(), unsafe_allow_html=True)

    def _get_custom_css(self):
        return """
        <style>
            .main {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            .header-text {
                background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 2rem;
            }
            .stock-card {
                background: white;
                border-radius: 15px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
                transition: transform 0.3s ease;
            }
            .stock-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.1);
            }
            .metric-container {
                background: white;
                border-radius: 10px;
                padding: 1rem;
                margin: 0.5rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .price-up {
                color: #10B981;
                background: rgba(16, 185, 129, 0.1);
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
            }
            .price-down {
                color: #EF4444;
                background: rgba(239, 68, 68, 0.1);
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
            }
            .chart-container {
                background: white;
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .stButton > button {
                background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                border: none;
                padding: 0.5rem 1.5rem;
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
        </style>
        """

    def fetch_stock_data(self, ticker: str) -> dict:
        """Fetch stock data from API"""
        try:
            response = requests.get(f"{self.backend_url}/analyze/{ticker}?analysis_type=overview")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None

    def safe_calculate_metrics(self, data: dict) -> dict:
        """Safely calculate metrics with fallback values"""
        try:
            if not data or 'stock_price_data' not in data:
                return {}

            hist_data = data['stock_price_data']['historical_prices']
            df = pd.DataFrame(hist_data['data'])
            if df.empty:
                return {}

            latest_price = float(df['Close'].iloc[-1])
            prev_price = float(df['Close'].iloc[-2]) if len(df) > 1 else latest_price
            price_change = latest_price - prev_price
            price_change_percent = (price_change / prev_price * 100) if prev_price != 0 else 0
            
            market_cap = data.get('market_data', {}).get('market_cap', 0)
            pe_ratio = data.get('trading_info', {}).get('pe_ratio', 0)
            dividend_yield = data.get('market_data', {}).get('dividend_yield', 0)

            return {
                'current_price': latest_price,
                'price_change': price_change,
                'price_change_percent': price_change_percent,
                'volume': float(df['Volume'].iloc[-1]) if 'Volume' in df else 0,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio,
                'dividend_yield': dividend_yield
            }
        except Exception:
            return {}

    def get_stock_data(self, ticker: str) -> dict:
        """Get stock data with caching"""
        try:
            if not ticker:
                return None
                
            data = self.cache.get_stock_data(ticker)
            if data is None:
                with st.spinner(f'Fetching data for {ticker}...'):
                    data = self.fetch_stock_data(ticker)
                    if data:
                        self.cache.store_stock_data(ticker, data)
            return data
        except Exception as e:
            print(f"Error getting stock data: {str(e)}")
            return None
    def create_charts(self, data: dict, ticker: str, compare_data: dict = None, compare_ticker: str = None):
        """Create separate charts for price, volume, and RSI"""
        try:
            # Process main stock data
            df = pd.DataFrame(data['stock_price_data']['historical_prices']['data'])
            df.index = pd.to_datetime(data['stock_price_data']['historical_prices']['index'])

            # Create price chart
            price_fig = go.Figure()
            price_fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Close'],
                name=f"{ticker} Price",
                line=dict(width=2, color=self.colors['primary'])
            ))

            if compare_data and compare_ticker:
                compare_df = pd.DataFrame(compare_data['stock_price_data']['historical_prices']['data'])
                compare_df.index = pd.to_datetime(compare_data['stock_price_data']['historical_prices']['index'])
                price_fig.add_trace(go.Scatter(
                    x=compare_df.index,
                    y=compare_df['Close'],
                    name=f"{compare_ticker} Price",
                    line=dict(width=2, color=self.colors['secondary'])
                ))

            price_fig.update_layout(
                title="Price History",
                height=400,
                showlegend=True,
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis_title="Price ($)",
                hovermode='x unified'
            )

            # Create volume chart
            volume_fig = go.Figure()
            colors = [self.colors['success'] if c >= o else self.colors['danger']
                     for c, o in zip(df['Close'], df['Open'])]
            
            volume_fig.add_trace(go.Bar(
                x=df.index,
                y=df['Volume'],
                name=f"{ticker} Volume",
                marker_color=colors,
                opacity=0.7
            ))

            if compare_data and compare_ticker:
                compare_colors = [self.colors['success'] if c >= o else self.colors['danger']
                                for c, o in zip(compare_df['Close'], compare_df['Open'])]
                volume_fig.add_trace(go.Bar(
                    x=compare_df.index,
                    y=compare_df['Volume'],
                    name=f"{compare_ticker} Volume",
                    marker_color=compare_colors,
                    opacity=0.5
                ))

            volume_fig.update_layout(
                title="Volume Analysis",
                height=300,
                showlegend=True,
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis_title="Volume",
                hovermode='x unified'
            )

            # Create RSI chart
            def calculate_rsi(prices, period=14):
                delta = prices.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
                rs = gain / loss
                return 100 - (100 / (1 + rs))

            rsi_fig = go.Figure()
            rsi = calculate_rsi(df['Close'])
            rsi_fig.add_trace(go.Scatter(
                x=df.index,
                y=rsi,
                name=f"{ticker} RSI",
                line=dict(color='purple', width=2)
            ))

            if compare_data and compare_ticker:
                compare_rsi = calculate_rsi(compare_df['Close'])
                rsi_fig.add_trace(go.Scatter(
                    x=compare_df.index,
                    y=compare_rsi,
                    name=f"{compare_ticker} RSI",
                    line=dict(color='orange', width=2)
                ))

            # Add RSI levels
            rsi_fig.add_hline(y=70, line_dash="dash", line_color="red",
                            annotation_text="Overbought")
            rsi_fig.add_hline(y=30, line_dash="dash", line_color="green",
                            annotation_text="Oversold")

            rsi_fig.update_layout(
                title="RSI Indicator",
                height=300,
                showlegend=True,
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis_title="RSI",
                hovermode='x unified'
            )

            # Update all charts with common styling
            for fig in [price_fig, volume_fig, rsi_fig]:
                fig.update_layout(
                    font=dict(family="Arial", size=12),
                    margin=dict(l=10, r=10, t=40, b=10),
                    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
                )

            return price_fig, volume_fig, rsi_fig

        except Exception as e:
            print(f"Error creating charts: {str(e)}")
            return None, None, None

    def display_metric_comparison(self, data1: dict, data2: dict, ticker1: str, ticker2: str):
        """Display side-by-side metric comparison"""
        try:
            metrics1 = self.safe_calculate_metrics(data1)
            metrics2 = self.safe_calculate_metrics(data2)

            col1, col2 = st.columns(2)
            with col1:
                self.display_animated_metrics(data1, ticker1, metrics1)
            with col2:
                self.display_animated_metrics(data2, ticker2, metrics2)
        except Exception as e:
            print(f"Error in metric comparison: {str(e)}")

    def display_animated_metrics(self, data: dict, ticker: str, metrics: dict = None):
        """Display animated metrics with error handling"""
        try:
            if metrics is None:
                metrics = self.safe_calculate_metrics(data)
            
            if not metrics:
                return

            st.markdown(f"""
            <div class="stock-card" style="background: linear-gradient(135deg, {self.colors['primary']} 0%, {self.colors['secondary']} 100%);">
                <div style="color: white;">
                    <h2>{ticker} - {self.cache.default_stocks.get(ticker, 'Stock Analysis')}</h2>
                    <div style="font-size: 2.5rem; margin: 1rem 0;">
                        ${metrics['current_price']:.2f}
                        <span class="{'price-up' if metrics['price_change'] >= 0 else 'price-down'}" 
                              style="font-size: 1.5rem; margin-left: 1rem;">
                            {'+' if metrics['price_change'] >= 0 else ''}{metrics['price_change']:.2f} 
                            ({'+' if metrics['price_change_percent'] >= 0 else ''}{metrics['price_change_percent']:.2f}%)
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(4)
            metrics_data = [
                ("Volume", f"{metrics['volume']:,.0f}"),
                ("Market Cap", f"${metrics['market_cap']/1e9:.2f}B"),
                ("P/E Ratio", f"{metrics['pe_ratio']:.2f}"),
                ("Dividend Yield", f"{metrics['dividend_yield']*100:.2f}%")
            ]

            for col, (label, value) in zip(cols, metrics_data):
                with col:
                    st.markdown(f"""
                    <div class="metric-container">
                        <h4>{label}</h4>
                        <div style="font-size: 1.5rem; font-weight: bold;">{value}</div>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            print(f"Error displaying animated metrics: {str(e)}")

    def display_stock_cards(self):
        """Display interactive stock cards with animations"""
        try:
            stocks_data = self.cache.get_cached_stocks_data()
            
            st.markdown(f"""
            <div style="padding: 1rem; background: white; border-radius: 15px; margin-bottom: 2rem;">
                <h2 style="color: {self.colors['primary']}; margin-bottom: 1rem;">📊 Popular Stocks</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem;">
            """, unsafe_allow_html=True)
            
            for ticker, info in stocks_data.items():
                metrics = info.get('metrics', {})
                if metrics:
                    current_price = metrics.get('current_price', 0)
                    price_change_percent = metrics.get('price_change_percent', 0)
                    
                    change_color = self.colors['success'] if price_change_percent >= 0 else self.colors['danger']
                    
                    st.markdown(f"""
                    <div class="stock-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h3 style="margin: 0; color: {self.colors['primary']}">{ticker}</h3>
                                <p style="margin: 0.5rem 0; color: {self.colors['text']}">{info['name']}</p>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.5rem; font-weight: bold; color: {self.colors['primary']}">
                                    ${current_price:.2f}
                                </div>
                                <div style="color: {change_color}; padding: 0.25rem 0.5rem; 
                                            background: rgba({','.join(map(str, self.hex_to_rgb(change_color)))}, 0.1); 
                                            border-radius: 15px; display: inline-block;">
                                    {'+' if price_change_percent >= 0 else ''}{price_change_percent:.2f}%
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Analyze", key=f"analyze_{ticker}"):
                        st.session_state.selected_stock = ticker
                        return True
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            return False

        except Exception as e:
            print(f"Error displaying stock cards: {str(e)}")
            return False

    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert hex color to RGB values"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def run(self):
        """Main dashboard execution"""
        st.markdown("""
        <div class="header-text">
            <h1 style="font-size: 3rem;">📈 Stock Analysis Pro</h1>
            <p style="font-size: 1.2rem;">Advanced Stock Analysis & Visualization Platform</p>
        </div>
        """, unsafe_allow_html=True)

        # Stock selection section
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            ticker = st.text_input(
                "Enter Stock Ticker",
                value=st.session_state.selected_stock or "",
                placeholder="e.g., AAPL"
            ).upper()
        with col2:
            compare_ticker = st.text_input(
                "Compare with",
                placeholder="e.g., MSFT"
            ).upper()
        with col3:
            analyze = st.button("🔍 Analyze", use_container_width=True)

        # Analysis section
        if analyze or st.session_state.selected_stock:
            ticker = ticker or st.session_state.selected_stock
            st.session_state.selected_stock = None  # Reset after use
            
            if ticker:
                with st.spinner(f'Analyzing {ticker}...'):
                    data = self.get_stock_data(ticker)
                    if data:
                        if compare_ticker:
                            compare_data = self.get_stock_data(compare_ticker)
                            if compare_data:
                                self.display_metric_comparison(data, compare_data, ticker, compare_ticker)
                                price_fig, volume_fig, rsi_fig = self.create_charts(
                                    data, ticker, compare_data, compare_ticker
                                )
                        else:
                            self.display_animated_metrics(data, ticker)
                            price_fig, volume_fig, rsi_fig = self.create_charts(data, ticker)

                        if price_fig and volume_fig and rsi_fig:
                            st.plotly_chart(price_fig, use_container_width=True)
                            st.plotly_chart(volume_fig, use_container_width=True)
                            st.plotly_chart(rsi_fig, use_container_width=True)

        # Popular stocks section
        if self.display_stock_cards():
            st.rerun()

if __name__ == "__main__":
    dashboard = StockDashboard()
    dashboard.run()
