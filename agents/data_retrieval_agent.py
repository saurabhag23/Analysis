# data_retrieval_agent.py
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
class DataConverter:
    @staticmethod
    def convert(obj):
        if obj is None:
            return None
        elif isinstance(obj, (str, int, bool)):
            return obj
        elif isinstance(obj, float):
            return obj if not np.isnan(obj) else None
        elif isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj) if not np.isnan(obj) else None
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, (np.datetime64, pd.Timestamp)):
            return pd.Timestamp(obj).isoformat()
        elif isinstance(obj, pd.Series):
            return {
                'name': obj.name,
                'data': {str(k): DataConverter.convert(v) for k, v in obj.items()}
            }
        elif isinstance(obj, pd.DataFrame):
            return {
                'columns': obj.columns.tolist(),
                'index': [str(idx) for idx in obj.index.tolist()],
                'data': [
                    {str(col): DataConverter.convert(val) for col, val in row.items()}
                    for row in obj.to_dict('records')
                ]
            }
        elif isinstance(obj, dict):
            return {str(k): DataConverter.convert(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, np.ndarray)):
            return [DataConverter.convert(x) for x in obj]
        elif pd.isna(obj):
            return None
        return str(obj)

class DataRetrievalAgent:
    def __init__(self, ticker,sec_api_key):
        """
        Initialize the agent with a stock ticker.
        
        Args:
            ticker (str): Stock ticker symbol
        """
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info
        self.sec_api_key = sec_api_key
        self.base_url = "https://data.sec.gov/api"
        self.headers = {
            "User-Agent": "agrawalsaurabhsunil@gmail.com",
            "Accept-Encoding": "gzip, deflate",
            "Host": "data.sec.gov"
        }

    def get_stock_price_data(self):
        """Fetch current and historical stock price data"""
        data = {
            "current_price": self.info.get('regularMarketPrice'),
            "historical_prices": self.stock.history(period="1y"),
            "price_change": self.info.get('regularMarketChange'),
            "price_change_percent": self.info.get('regularMarketChangePercent')
        }
        return DataConverter.convert(data)

    def get_market_data(self):
        """Retrieve market-related data"""
        data = {
            "market_cap": self.info.get('marketCap'),
            "dividend_yield": self.info.get('dividendYield'),
            "dividend_rate": self.info.get('dividendRate'),
            "52_week_high": self.info.get('fiftyTwoWeekHigh'),
            "52_week_low": self.info.get('fiftyTwoWeekLow')
        }
        return DataConverter.convert(data)

    def get_trading_info(self):
        """Fetch trading-related information"""
        data = {
            "volume": self.info.get('volume'),
            "average_volume": self.info.get('averageVolume'),
            "beta": self.info.get('beta'),
            "pe_ratio": self.info.get('trailingPE'),
            "forward_pe": self.info.get('forwardPE'),
            "eps": self.info.get('trailingEps')
        }
        return DataConverter.convert(data)

    def get_financial_statements(self):
        """Retrieve financial statements"""
        data = {
            "income_statement": self.stock.financials,
            "balance_sheet": self.stock.balance_sheet,
            "cash_flow": self.stock.cashflow,
            "quarterly_financials": self.stock.quarterly_financials,
            "quarterly_balance_sheet": self.stock.quarterly_balance_sheet,
            "quarterly_cashflow": self.stock.quarterly_cashflow
        }
        return DataConverter.convert(data)

    def get_analyst_data(self):
        data = {
            "analyst_recommendations": self.stock.recommendations,
            "analyst_price_target": self.info.get('targetMeanPrice'),
            "net_income": self.stock.income_stmt.get('Net Income') if isinstance(self.stock.income_stmt, dict) else None
        }
        return DataConverter.convert(data)

    def get_company_info(self):
        """Retrieve detailed company information"""
        data = {
            "sector": self.info.get('sector'),
            "industry": self.info.get('industry'),
            "full_time_employees": self.info.get('fullTimeEmployees'),
            "business_summary": self.info.get('longBusinessSummary')
        }
        return DataConverter.convert(data)

    def get_performance_metrics(self):
        """Fetch various performance metrics"""
        data = {
            "return_on_assets": self.info.get('returnOnAssets'),
            "return_on_equity": self.info.get('returnOnEquity'),
            "profit_margins": self.info.get('profitMargins')
        }
        return DataConverter.convert(data)

    def get_technical_indicators(self):
        """Calculate and return technical indicators"""
        hist = self.stock.history(period="6mo")
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
        
        # RSI calculation
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        hist['EMA_12'] = hist['Close'].ewm(span=12, adjust=False).mean()
        hist['EMA_26'] = hist['Close'].ewm(span=26, adjust=False).mean()
        hist['MACD'] = hist['EMA_12'] - hist['EMA_26']
        hist['Signal_Line'] = hist['MACD'].ewm(span=9, adjust=False).mean()

        return DataConverter.convert(hist)

    def get_options_data(self):
        """Retrieve options data"""
        expirations = self.stock.options[:2]  # Get first two expiration dates
        data = {date: self.stock.option_chain(date) for date in expirations}
        return DataConverter.convert(data)

    def get_ownership_data(self):
        """Fetch institutional and major holders data"""
        data = {
            "major_holders": self.stock.major_holders,
            "institutional_holders": self.stock.institutional_holders
        }
        return DataConverter.convert(data)

    def get_sustainability_score(self):
        """Retrieve ESG scores"""
        return DataConverter.convert(self.stock.sustainability)

    def get_valuation_measures(self):
        """Retrieve key valuation measures"""
        data = {
            "price_to_book": self.info.get('priceToBook'),
            "enterprise_to_ebitda": self.info.get('enterpriseToEbitda')
        }
        return DataConverter.convert(data)

    def get_stock_events(self):
        """Fetch stock events like splits and dividends"""
        data = {
            "splits": self.stock.splits,
            "dividends": self.stock.dividends,
            "actions": self.stock.actions
        }
        return DataConverter.convert(data)
    '''def get_cik(self):
        url = f"{self.base_url}/xbrl/companyfacts/{self.ticker}.json"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['cik']
        else:
            raise Exception(f"Failed to retrieve CIK for {self.ticker}")'''

    def get_company_facts(self):
        cik = 789019
        url = f"{self.base_url}/xbrl/companyfacts/CIK{cik:010d}.json"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        #else:
        #    raise Exception(f"Failed to retrieve company facts for {self.ticker}")

    def get_latest_10k(self):
        cik = 789019
        url = f"{self.base_url}/submissions/CIK{cik:010d}.json"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            for filing in data['filings']['recent']:
                if filing['form'] == '10-K':
                    return filing
        #raise Exception(f"No 10-K filing found for {self.ticker}")

    def get_latest_10q(self):
        cik = 789019
        url = f"{self.base_url}/submissions/CIK{cik:010d}.json"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            for filing in data['filings']['recent']:
                if filing['form'] == '10-Q':
                    return filing
        #raise Exception(f"No 10-Q filing found for {self.ticker}")

    def get_segment_information(self):
        company_facts = self.get_company_facts()
        segment_data = {}
        for fact in company_facts['facts'].get('us-gaap', {}):
            if 'Segment' in fact:
                segment_data[fact] = company_facts['facts']['us-gaap'][fact]
        return DataConverter.convert(segment_data)

    def get_equity_structure(self):
        company_facts = self.get_company_facts()
        equity_data = {}
        for fact in company_facts['facts'].get('us-gaap', {}):
            if 'ShareholdersEquity' in fact or 'StockIssuedDuringPeriod' in fact:
                equity_data[fact] = company_facts['facts']['us-gaap'][fact]
        return DataConverter.convert(equity_data)

    def get_sec_edgar_data(self):
        """Comprehensive method to fetch all SEC EDGAR data"""
        data = {
            "company_facts": self.get_company_facts(),
            "latest_10k": self.get_latest_10k(),
            "latest_10q": self.get_latest_10q(),
            "segment_information": self.get_segment_information(),
            "equity_structure": self.get_equity_structure()
        }
        return DataConverter.convert(data)
    def get_fundamental_data(self):
        
        data = {
            "financial_statements": self.get_financial_statements(),
            "company_info": self.get_company_info(),
            "market_data": self.get_market_data(),
            "analyst_data": self.get_analyst_data(),
            "performance_metrics": self.get_performance_metrics(),
            "valuation_measures": self.get_valuation_measures(),
            "ownership_data": self.get_ownership_data(),
            "sustainability_score": self.get_sustainability_score(),
            "sec_edgar_data": self.get_sec_edgar_data()
        }
        return DataConverter.convert(data)

    def get_technical_data(self):
        data = {
            "stock_price_data": self.get_stock_price_data(),
            "trading_info": self.get_trading_info(),
            "technical_indicators": self.get_technical_indicators(),
            "options_data": self.get_options_data(),
            "stock_events": self.get_stock_events(),
            "real_time_quote": DataConverter.convert(self.info)
        }
        return DataConverter.convert(data)
    
    def get_all_data(self):
        """Comprehensive method to fetch all available data"""
        data = {
            "stock_price_data": self.get_stock_price_data(),
            "market_data": self.get_market_data(),
            "trading_info": self.get_trading_info(),
            "financial_statements": self.get_financial_statements(),
            "analyst_data": self.get_analyst_data(),
            "company_info": self.get_company_info(),
            "performance_metrics": self.get_performance_metrics(),
            "technical_indicators": self.get_technical_indicators(),
            "options_data": self.get_options_data(),
            "ownership_data": self.get_ownership_data(),
            "sustainability_score": self.get_sustainability_score(),
            "valuation_measures": self.get_valuation_measures(),
            "stock_events": self.get_stock_events(),
            "real_time_quote": DataConverter.convert(self.info),
            "sec_edgar_data": self.get_sec_edgar_data()
        }
        return DataConverter.convert(data)