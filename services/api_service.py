from fastapi import APIRouter, HTTPException
from agents.coordination import CoordinationAgent

router = APIRouter()

@router.get("/analyze/{ticker}", response_model=dict)
async def analyze_ticker(ticker: str):
    coordination_agent = CoordinationAgent()
    try:
        result = coordination_agent.coordinate_analysis(ticker)
    except Exception as e:
        # Handles any exception that might occur during coordination or analysis
        raise HTTPException(status_code=500, detail=str(e))

    if "error" in result:
        # If the analysis results contain an error key, it implies something went wrong during analysis
        raise HTTPException(status_code=404, detail=result["error"])

    return result
