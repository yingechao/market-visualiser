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
      <h2>Portfolio Value</h2>

      <ResponsiveContainer>
        <LineChart data={results}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="date"
            minTickGap={50}
          />

          <YAxis
            tickFormatter={(value) => `$${value.toLocaleString()}`}
          />

          <Tooltip
            formatter={(value) => [
              `$${Number(value).toLocaleString()}`,
              "Portfolio Value"
            ]}
          />

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