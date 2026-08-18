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

interface DrawdownChartProps {
  results: BacktestResult[];
}

function DrawdownChart({ results }: DrawdownChartProps) {
  return (
    <div style={{ width: "100%", height: 400 }}>

      <h2>Drawdown</h2>

      <ResponsiveContainer>
        <LineChart data={results}>
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis
            dataKey="date"
            minTickGap={50}
        />

        <YAxis
            tickFormatter={(value) =>
            `${(value * 100).toFixed(1)}%`
            }
        />

        <Tooltip
            formatter={(value) => [
            `${(Number(value) * 100).toFixed(2)}%`,
            "Drawdown",
            ]}
        />

        <Line
            type="monotone"
            dataKey="drawdown"
            dot={false}
        />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default DrawdownChart;