from fastapi import FastAPI

from run_backtest import run_pipeline

app = FastAPI()

@app.get("/")
def root():
    return{
        "message": "Market visualiser API is running"
    }

@app.get("/backtest")
def get_backtest():
    data, signals, results, trades, summary = run_pipeline(
        filepath="../data/AAPL.csv", 
        initial_cash=10000,
    )

    return {
        "summary":summary, # not sure why we need to return this since the function should return stuff anyway
    }