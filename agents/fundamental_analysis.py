import openai
import pandas as pd
import numpy as np
from utils.config import OPENAI_API_KEY

class FundamentalAnalysisAgent:
    def __init__(self):
        self.openai_api_key = OPENAI_API_KEY

    def analyze_financials(self, financial_data, ticker):
        ratios = self.calculate_financial_ratios(financial_data)
        narrative = self.generate_financial_narrative(ratios, ticker)
        return {
            "ratios": ratios,
            "narrative": narrative
        }

    def calculate_financial_ratios(self, financial_data):
        ratios = {}
        
        # Financial Statements
        income_statement = self.convert_to_df(financial_data.get('financial_statements', {}).get('income_statement'))
        balance_sheet = self.convert_to_df(financial_data.get('financial_statements', {}).get('balance_sheet'))
        cash_flow = self.convert_to_df(financial_data.get('financial_statements', {}).get('cash_flow'))

        # Market Data
        market_data = financial_data.get('market_data', {})
        
        # Company Info
        company_info = financial_data.get('company_info', {})
        
        # Performance Metrics
        performance_metrics = financial_data.get('performance_metrics', {})
        
        # Valuation Measures
        valuation_measures = financial_data.get('valuation_measures', {})

        def safe_divide(a, b):
            if pd.isna(a) or pd.isna(b) or b == 0:
                return np.nan
            return a / b

        def get_latest_value(df, row_name):
            if df is None or df.empty:
                return np.nan
            
            if isinstance(df, pd.DataFrame):
                if row_name in df.index:
                    series = df.loc[row_name]
                    return series.dropna().iloc[-1] if not series.empty else np.nan
            elif isinstance(df, dict):
                if 'data' in df and row_name in df['data']:
                    values = [v for v in df['data'][row_name].values() if v is not None]
                    return values[-1] if values else np.nan
            return np.nan

        # Profitability Ratios
        ratios['ROE'] = performance_metrics.get('return_on_equity')
        ratios['ROA'] = performance_metrics.get('return_on_assets')
        ratios['Profit Margin'] = performance_metrics.get('profit_margins')
        
        # Liquidity Ratios
        current_assets = get_latest_value(balance_sheet, 'Total Current Assets')
        current_liabilities = get_latest_value(balance_sheet, 'Total Current Liabilities')
        ratios['Current Ratio'] = safe_divide(current_assets, current_liabilities)
        
        # Solvency Ratios
        total_liabilities = get_latest_value(balance_sheet, 'Total Liabilities')
        total_equity = get_latest_value(balance_sheet, "Total Stockholders' Equity")
        ratios['Debt to Equity'] = safe_divide(total_liabilities, total_equity)
        
        # Efficiency Ratios
        total_revenue = get_latest_value(income_statement, 'Total Revenue')
        total_assets = get_latest_value(balance_sheet, 'Total Assets')
        ratios['Asset Turnover'] = safe_divide(total_revenue, total_assets)
        
        # Market Ratios
        ratios['P/E Ratio'] = valuation_measures.get('price_to_book')
        ratios['Dividend Yield'] = market_data.get('dividend_yield')
        
        # Growth Rates
        if income_statement is not None and not income_statement.empty:
            try:
                revenue_series = self.get_series_from_df(income_statement, 'Total Revenue')
                net_income_series = self.get_series_from_df(income_statement, 'Net Income')
                
                if revenue_series is not None:
                    ratios['Revenue Growth Rate'] = revenue_series.pct_change().mean()
                if net_income_series is not None:
                    ratios['Net Income Growth Rate'] = net_income_series.pct_change().mean()
            except Exception as e:
                print(f"Error calculating growth rates: {e}")

        # Cash Flow Metrics
        if cash_flow is not None and not cash_flow.empty:
            operating_cash_flow = get_latest_value(cash_flow, 'Operating Cash Flow')
            capital_expenditures = get_latest_value(cash_flow, 'Capital Expenditure')
            if not pd.isna(operating_cash_flow) and not pd.isna(capital_expenditures):
                ratios['Free Cash Flow'] = operating_cash_flow - capital_expenditures

        # Remove any NaN values
        ratios = {k: v for k, v in ratios.items() if not pd.isna(v)}

        return ratios

    def convert_to_df(self, data):
        """Convert dictionary data to DataFrame if necessary."""
        if data is None:
            return pd.DataFrame()
        
        if isinstance(data, pd.DataFrame):
            return data
            
        if isinstance(data, dict):
            if 'data' in data and 'columns' in data and 'index' in data:
                df_data = pd.DataFrame(data['data'])
                df_data.index = data['index']
                return df_data
            
        return pd.DataFrame()

    def get_series_from_df(self, df, row_name):
        """Safely extract a series from DataFrame for calculation."""
        if isinstance(df, pd.DataFrame) and row_name in df.index:
            return df.loc[row_name]
        return None

    def generate_financial_narrative(self, financial_ratios, company_name):
        prompt = f"Financial Analysis for {company_name}\n\n"
        prompt += "Based on the current financial data, here is an in-depth analysis of the company's financial performance:\n\n"
        
        for ratio, value in financial_ratios.items():
            if isinstance(value, float):
                prompt += f"- {ratio}: {value:.2f}\n"
            else:
                prompt += f"- {ratio}: {value}\n"

        prompt += "\n\nPlease analyze these metrics to provide insights into the company's financial stability, profitability, operational efficiency, and potential financial risks or opportunities."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analyst providing insights."},
                {"role": "user", "content": prompt}
            ],
            api_key=self.openai_api_key
        )
        narrative = response['choices'][0]['message']['content'] if response['choices'] else "No narrative generated."
        return narrative