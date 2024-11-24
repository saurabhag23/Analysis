from agents.data_retrieval_agent import DataRetrievalAgent
from agents.fundamental_analysis import FundamentalAnalysisAgent
from agents.technical_analysis import TechnicalAnalysisAgent
from utils.config import SEC_API_KEY


class CoordinationAgent:
    def __init__(self):
        """
        Initializes the CoordinationAgent.
        This agent manages the interactions of various agents.
        """
        pass

    def coordinate_analysis(self, ticker, analysis_type='both'):
        """
        Coordinates the fetching of data and the analysis process for a given ticker.
        :param ticker: str, the stock ticker symbol.
        :param analysis_type: str, type of analysis ('fundamental', 'technical', 'both').
        :return: dict, the results of the analysis including data from various agents.
        """
        data_agent = DataRetrievalAgent(ticker,SEC_API_KEY)
        
        if analysis_type == 'overview':
            return data_agent.get_all_data()
        
        
        results = {}
        if analysis_type == 'fundamental' or analysis_type == 'both':
            financial_data = data_agent.get_fundamental_data()
            fundamental_agent = FundamentalAnalysisAgent()
            results['Fundamental Analysis'] = fundamental_agent.analyze_financials(financial_data, ticker)

        if analysis_type == 'technical' or analysis_type == 'both':
            financial_data = data_agent.get_technical_data()
            technical_agent = TechnicalAnalysisAgent()
            results['Technical Analysis'] = technical_agent.analyze_technical(financial_data)

        return results