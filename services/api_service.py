from fastapi import APIRouter, HTTPException, Query
from agents.coordination import CoordinationAgent

router = APIRouter()

@router.get("/analyze/{ticker}")
async def analyze_ticker(ticker: str, analysis_type: str = Query('both', enum=['fundamental', 'technical', 'both','overview'])):
    """
    Endpoint to analyze a stock ticker with specified analysis type.
    :param ticker: str, the stock ticker symbol.
    :param analysis_type: str, type of analysis to perform ('fundamental', 'technical', 'both').
    :return: dict, the results of the analysis.
    """
    coordination_agent = CoordinationAgent()
    try:
        result = coordination_agent.coordinate_analysis(ticker, analysis_type)
    except Exception as e:
        # Handles any exception that might occur during coordination or analysis
        raise HTTPException(status_code=500, detail=str(e))

    if "error" in result:
        # If the analysis results contain an error key, it implies something went wrong during analysis
        raise HTTPException(status_code=404, detail=result["error"])

    return result