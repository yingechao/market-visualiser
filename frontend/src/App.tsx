// Loads the JSON and displays the dashboard
import { useState } from "react";
import type { BacktestResponse } from "./types";
import PortfolioChart from "./components/PortfolioChart";
import PriceChart from "./components/PriceChart";
import DrawdownChart from "./components/drawdownChart";

import "./styles.css";

function App(){

    const[backtest, setBacktest] = useState < BacktestResponse | null > (null); // asks react to remember this state and sets it to null

    async function runBacktest(){
        const response = await fetch("http://127.0.0.1:8000/backtest"); // react sends HTTP GET request to Python
        // likely to change for deployment***
        if (!response.ok){
            throw new Error("Backtest failed");
        }

        const data: BacktestResponse = await response.json(); // convert the response body from JSON to a Javascript object

        console.log(data);
        console.log(data.results[0]);
        setBacktest(data); 


    }

return (
  <div>
    <button onClick={runBacktest}>
      Run Backtest
    </button>

    {backtest && (
    <div>
        <h2>Backtest Results</h2>

        <p>
        Starting value: {backtest.summary.starting_value}
        </p>

        <p>
        Ending value: {backtest.summary.ending_value}
        </p>
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

