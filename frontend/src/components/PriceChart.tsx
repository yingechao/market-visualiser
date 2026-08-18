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

interface PriceChartProps {
  results: BacktestResult[];
}

function PriceChart({ results }: PriceChartProps) {
  return (
    <div style={{ width: "100%", height: 400 }}>

      <h2>Price Value</h2>

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
              "Asset Value"
            ]}
          />

          <Line
            type="monotone"
            dataKey="close"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PriceChart;