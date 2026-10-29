# Market visualiser

A local market backtesting and visualisation project using Python, pandas, FastAPI, React and TypeScript. It simulates a 20/50-day moving-average strategy over historical prices and compares the resulting portfolio with a buy-and-hold benchmark.

## Run locally

From the project root, set up the Python environment (Python 3.10 or newer):

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r python/requirements.txt
```

Start the API in the first terminal:

```bash
cd python
python -m uvicorn api:app --reload --port 8000
```

In a second terminal, from the project root, install and start the frontend:

```bash
cd frontend
npm install
npm run dev -- --port 5173
```

Open http://localhost:5173, enter an optional transaction cost percentage per trade, and select **Run Backtest**. Keep both servers running. The included AAPL CSV is used by default; no download is required. The API can also be started from the project root with `venv/bin/python -m uvicorn api:app --app-dir python --port 8000`.

To run the alternative Streamlit dashboard, activate the environment and run `streamlit run python/app.py` from the project root.

## Model assumptions

- The strategy uses 20- and 50-session moving averages of closing prices to decide whether to hold the asset or cash. A change in position is executed at the next session’s open, subject to available cash.
- The portfolio holds one asset or cash, with no short selling or fractional shares. Prices and dates come from the included historical CSV.
- Transaction costs are a percentage of trade value, paid on each purchase and sale; they default to zero. The model does not include slippage or other execution effects.
- The buy-and-hold benchmark attempts to purchase at the second session’s open, the earliest execution supported by the simulator. The moving-average strategy requires 50 sessions of price history before it can generate a buy signal. Both use the same initial cash, whole-share rules and transaction-cost rate. Remaining holdings are valued at the final close without being sold.
- These are historical simulations, not evidence of future performance. The data cleaner validates prices but does not model corporate actions or verify the source's adjustment methodology.

The Python `run_pipeline(filepath, initial_cash, transaction_cost_rate)` function accepts another OHLCV CSV and starting balance. The API accepts `transaction_cost_rate` as a decimal fraction; for example, `0.001` means 0.1% per trade.

## Correctness tests

From the project root, run:

```bash
venv/bin/python -m pytest -q
```

The tests use small synthetic datasets and hand-calculated expected results. They cover execution timing, cash and position accounting, transaction costs, the benchmark, returns, drawdowns and input validation. They do not require a running server or market-data download.
