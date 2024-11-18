# agents/coordination_agent.py
from agents.data_retrieval_agent import DataRetrievalAgent
from agents.fundamental_analysis import FundamentalAnalysisAgent
from agents.technical_analysis import TechnicalAnalysisAgent
# If you have a TechnicalAnalysisAgent, you might want to include it as well

class CoordinationAgent:
    def __init__(self):
        """
        Initializes the CoordinationAgent.
        This agent does not require specific initialization parameters but manages the interactions of various agents.
        """
        pass

    def coordinate_analysis(self, ticker):
        """
        Coordinates the fetching of data and the analysis process for a given ticker.
        :param ticker: str, the stock ticker symbol.
        :return: dict, the results of the analysis including data from various agents.
        """
        # Create an instance of the Data Retrieval Agent to fetch data
        data_agent = DataRetrievalAgent(ticker)
        financial_data = data_agent.get_all_data()  # Fetch all relevant financial data

        # Pass the fetched data to the Fundamental Analysis Agent
        fundamental_agent = FundamentalAnalysisAgent()
        fundamental_results = fundamental_agent.analyze_financials(financial_data,ticker)
        
        technical_agent = TechnicalAnalysisAgent()
        technical_results = technical_agent.analyze_technical(financial_data['historical_prices'])
        # If technical analysis is part of your system, you could do something similar here
        # technical_agent = TechnicalAnalysisAgent()
        # technical_results = technical_agent.analyze_technical(financial_data['historical_prices'])

        # Combine results from different agents if needed and return
        results = {
            "Fundamental Analysis": fundamental_results,
            "Technical Analysis": technical_results
            # "Technical Analysis": technical_results if technical analysis is included
        }
        return results
