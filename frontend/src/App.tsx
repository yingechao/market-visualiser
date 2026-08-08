// Loads the JSON and displays the dashboard
import { useState } from "react";
import type { BacktestResponse } from "./types";

function App(){

    const[backtest, setBacktest] = useState < BacktestResponse | null > (null); // asks react to remember this state and sets it to null

    async function runBacktest(){
        const response = await fetch("http://127.0.0.1:8000/backtest");
        if (!response.ok){
            throw new Error("Backtest failed");
        }

        const data: BacktestResponse = await response.json();

        console.log(data);
        setBacktest(data);

    }

    return(
        <div>
            <h1>Market Visualiser</h1>

            <button onClick={runBacktest}>
                
            </button>
        </div>
    )



}