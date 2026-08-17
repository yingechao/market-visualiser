import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

import type { BacktestResult } from "../types";

interface PortfolioChartProps {
  results: BacktestResult[];
}

function PortfolioChart({ results }: PortfolioChartProps) {
  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer>
        <LineChart data={results}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="date" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="portfolio_value"
            dot={false}
          />

        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PortfolioChart;