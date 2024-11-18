# agents/data_retrieval_agent.py
import yfinance as yf

class DataRetrievalAgent:
    def __init__(self, ticker):
        """
        Initializes the agent with the stock ticker to fetch data for.
        :param ticker: str, stock ticker symbol.
        """
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_historical_prices(self, period="max", interval="1d"):
        """
        Fetches historical stock prices.
        :param period: str, period for which to fetch historical data ('1d', '1mo', '1y', '5y', 'max').
        :param interval: str, data interval ('1d' for daily, '1wk' for weekly, '1mo' for monthly).
        :return: DataFrame, historical stock prices.
        """
        return self.stock.history(period=period, interval=interval)

    def get_financial_statements(self):
        """
        Retrieves the financial statements: income statement, balance sheet, and cash flow statement.
        :return: dict, containing DataFrames for the financial statements.
        """
        '''
        income_statement = self.stock.financials
        balance_sheet = self.stock.balance_sheet
        cash_flow = self.stock.cashflow
        print("Income Statement Row Labels:\n", income_statement.index)
        print("Balance Sheet Row Labels:\n", balance_sheet.index)
        print("Cash Flow Row Labels:\n", cash_flow.index)'''
        income_statement = self.stock.financials
        balance_sheet = self.stock.balance_sheet
        
        return {
            "income_statement": self.stock.financials,
            "balance_sheet": self.stock.balance_sheet,
            "cash_flow": self.stock.cashflow
        }

    def get_dividends_and_splits(self):
        """
        Fetches the history of dividends and stock splits.
        :return: DataFrame, history of dividends and stock splits.
        """
        return {
            "dividends": self.stock.dividends,
            "splits": self.stock.splits
        }

    def get_all_data(self):
        """
        A comprehensive method to fetch all required data for analysis.
        :return: dict, all relevant financial data.
        """
        return {
            "historical_prices": self.get_historical_prices(),
            "financial_statements": self.get_financial_statements(),
            "dividends_and_splits": self.get_dividends_and_splits()
        }
