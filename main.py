from fastapi import FastAPI
from services.api_service import router as api_router

app = FastAPI(title="Investment Analyst AI")

@app.get("/", response_model=str)
def read_root():
    return "Welcome to the Investment Analyst AI System!"


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000)
