// Loads the JSON and displays the dashboard
import { useState } from "react";
import type { BacktestResponse } from "./types";
import PortfolioChart from "./components/PortfolioChart";
import PriceChart from "./components/PriceChart";
import DrawdownChart from "./components/drawdownChart";

import "./styles.css";

function App(){

    const[backtest, setBacktest] = useState < BacktestResponse | null > (null); // asks react to remember this state and sets it to null
    const [costPercent, setCostPercent] = useState("0");
    const [error, setError] = useState("");

    async function runBacktest(){
        const percent = Number(costPercent);
        if (costPercent.trim() === "" || !Number.isFinite(percent) || percent < 0 || percent >= 100) {
            setError("Enter a transaction cost between 0% and less than 100%.");
            return;
        }
        setError("");
        try {
        const response = await fetch(`http://127.0.0.1:8000/backtest?transaction_cost_rate=${percent / 100}`);
        // likely to change for deployment***
        if (!response.ok){
            throw new Error("Backtest failed");
        }

        const data: BacktestResponse = await response.json(); // convert the response body from JSON to a Javascript object

        setBacktest(data); 
        } catch {
            setError("Could not run the backtest. Check that the backend is running.");
        }

    }

return (
  <div>
    <label>Transaction cost per trade (%) <input type="number" min="0" max="99.99" step="0.01" value={costPercent} onChange={(event) => setCostPercent(event.target.value)} /></label>
    <button onClick={runBacktest}>
      Run Backtest
    </button>
    {error && <p role="alert">{error}</p>}

    {backtest && (
    <div>
        <h2>Backtest Results</h2>

        <p>
        Starting value: {backtest.summary.starting_value}
        </p>

        <p>
        Ending value: {backtest.summary.ending_value}
        </p>
        <p>Buy-and-hold ending value: {backtest.summary.benchmark_ending_value.toFixed(2)}</p>
        <p>Strategy return: {(backtest.summary.total_return * 100).toFixed(2)}%; buy-and-hold return: {(backtest.summary.benchmark_total_return * 100).toFixed(2)}%</p>
        <div className="charts">

        <PortfolioChart results={backtest.results} />

        <DrawdownChart results={backtest.results} />
        
        <PriceChart 
        results = {backtest.results} 
        trades = {backtest.trades}
        />
        </div>
    </div>
    )}
    
  </div>
);

}

export default App;

