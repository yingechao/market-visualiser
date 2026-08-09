from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from run_backtest import run_pipeline


app = FastAPI()

# CORS section likely to change for deployment ************************
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5174",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# defines what happens when someone sends a GET request to : http://localhost:8000/
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
    # convert the results into a dict
    results_json = results.reset_index() # resetting index brings the DataFrame index of results to a normal column which is easier to send the the frontend
    # convert dates into strings
    results_json["date"] = (results_json["date"].dt.strftime("%Y-%m-%d"))
    #convert to JSON
    results_json = results_json.to_dict(orient="records")

    trades_json = trades.copy()

    if not trades_json.empty:
        trades_json["date"] = (trades_json["date"].dt.strftime("%Y-%m-%d"))

    trades_json = trades_json.to_dict(orient="records")

    return {
        "summary":summary, # not sure why we need to return this since the function should return stuff anyway
        "results":results_json, 
        "trades":trades_json,
    }