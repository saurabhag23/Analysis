# agents/fundamental_analysis_agent.py
import openai
from utils.config import OPENAI_API_KEY

class FundamentalAnalysisAgent:
    def __init__(self):
        """
        Initializes the FundamentalAnalysisAgent with the necessary OpenAI API key.
        """
        self.openai_api_key = OPENAI_API_KEY

    def analyze_financials(self, financial_data,ticker):
        """
        Analyzes financial data to calculate key financial ratios and generate a narrative.
        :param financial_data: dict, comprehensive financial data including historical prices, statements, and dividends.
        :return: dict, analysis results including financial ratios and a narrative summary.
        """
        financial_statements = financial_data['financial_statements']
        ratios = self.calculate_financial_ratios(financial_statements)
        narrative = self.generate_financial_narrative(ratios,ticker)
        return {
            "ratios": ratios,
            "narrative": narrative
        }

    def calculate_financial_ratios(self, financial_statements):
        income_statement = financial_statements['income_statement']
        balance_sheet = financial_statements['balance_sheet']
        cash_flow = financial_statements['cash_flow']

        # Access metrics directly by row label
        print("Income Statement:\n", income_statement.loc['Net Income'])
        print("Balance Sheet for Stockholders Equity:\n", balance_sheet.loc['Stockholders Equity'])
        def get_latest_value(series):
        # This function retrieves the latest non-NaN value or returns 0 if all are NaN
            return series.dropna().iloc[-1] if not series.dropna().empty else 0

        net_income = income_statement.loc['Net Income Continuous Operations'].iloc[-1]
        total_equity = balance_sheet.loc['Stockholders Equity'].iloc[-1]
        total_current_assets = balance_sheet.loc['Current Assets'].iloc[-1]
        total_current_liabilities = balance_sheet.loc['Current Liabilities'].iloc[-1]
        total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[-1]
        total_assets = balance_sheet.loc['Total Assets'].iloc[-1]
        operating_income = income_statement.loc['Operating Income'].iloc[-1]
        total_revenue = income_statement.loc['Total Revenue'].iloc[-1]


        # Calculate financial ratios
        roe = net_income / total_equity
        eps = net_income / income_statement.loc['Diluted Average Shares'].iloc[-1]
        current_ratio = total_current_assets / total_current_liabilities 
        debt_to_equity_ratio = total_liabilities / total_equity 
        gross_profit_margin = (total_revenue - income_statement.loc['Cost Of Revenue'].iloc[-1]) / total_revenue 
        operating_margin = operating_income / total_revenue 
        roa = net_income / total_assets 

        ratios = {
            "ROE": roe,
            "EPS": eps,
            "Current Ratio": current_ratio,
            "Debt to Equity Ratio": debt_to_equity_ratio,
            "Gross Profit Margin": gross_profit_margin,
            "Operating Margin": operating_margin,
            "ROA": roa
        }
        return ratios

    def generate_financial_narrative(self, financial_ratios,company_name):
        """
        Generates a narrative summary of the financial health using OpenAI's GPT model based on calculated financial ratios.
        """
        prompt = f"Financial Analysis for {company_name}\n\n"
        prompt += "Based on the current financial data, here is an in-depth analysis of the company's financial performance:\n\n"
        prompt += "\n".join([
            f"- Return on Equity (ROE): {financial_ratios['ROE']:.2%} indicates how effectively the company uses investments to generate earnings growth.",
            f"- Earnings Per Share (EPS): ${financial_ratios['EPS']:.2f} shows the portion of a company's profit allocated to each outstanding share of common stock, highlighting profitability on a per-share basis.",
            f"- Current Ratio: {financial_ratios['Current Ratio']:.2f}, which measures the company's ability to pay off its short-term liabilities with its short-term assets. A ratio above 1 suggests good short-term financial health.",
            f"- Debt to Equity Ratio: {financial_ratios['Debt to Equity Ratio']:.2f} shows the proportion of equity and debt the company uses to finance its assets, a lower ratio suggests less risk.",
            f"- Gross Profit Margin: {financial_ratios['Gross Profit Margin']:.2%} reflects the financial health of the company's core activities, indicating how efficiently it uses its resources.",
            f"- Operating Margin: {financial_ratios['Operating Margin']:.2%} demonstrates the percentage of revenue left after paying for variable production expenses, indicating the efficiency of the management.",
            f"- Return on Assets (ROA): {financial_ratios['ROA']:.2%} highlights how profitable a company is relative to its total assets, indicating how efficient management is at using its assets to generate earnings."
        ])

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

