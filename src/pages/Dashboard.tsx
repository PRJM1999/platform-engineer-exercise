import React, { useState, useEffect, useRef } from "react";
import { Line } from "react-chartjs-2";
import Select, { MultiValue, Options } from "react-select";
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

interface Option {
  value: string;
  label: string;
}

const stockOptions: Options<Option> = [
  { value: "IBM", label: "IBM" },
  { value: "TSCO.LON", label: "TSCO.LON" },
  { value: "SHOP.TRT", label: "SHOP.TRT" },
  { value: "GPV.TRV", label: "GPV.TRV" },
  { value: "MBG.DEX", label: "MBG.DEX" },
  { value: "RELIANCE.BSE", label: "RELIANCE.BSE" },
  { value: "600104.SHH", label: "600104.SHH" },
  { value: "000002.SHZ", label: "000002.SHZ" },
];

const Dashboard: React.FC = () => {
  const [selectedOptions, setSelectedOptions] = useState<MultiValue<Option>>([]);
  const [chartData, setChartData] = useState<{
    label: string;
    data: number[];
    dates: Date[];
  }[]>([]);
  const chartRef = useRef<Chart<"line", number[], string> | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const data = await Promise.all(
        selectedOptions.map(async (option) => {
          const response = await fetch(
            `http://localhost:3000/load_data?symbol=${option.value}`
          );
          const json = await response.json();
          return {
            label: option.label,
            data: json.value,
            dates: json.dates.map((dateStr: string) => new Date(dateStr)),
          };
        })
      );
      setChartData(data);
    };

    fetchData();
  }, [selectedOptions]);

  useEffect(() => {
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    if (chartData.length > 0) {
      const newChartInstance = new Chart("chart", {
        type: "line",
        data: {
          labels: chartData[0].dates.map((date) => date.toLocaleDateString()),
          datasets: chartData.map((data) => ({
            label: data.label,
            data: data.data
          })),
        },
        options: {
            scales: {
                x: {
                    reverse: true, 
                    title: {
                        display: true,
                        text: "Time"
                    }
                },
                y : {
                    title: {
                        display: true,
                        text: "Price ($)"
                    }
                }
            }
        }
      });

      chartRef.current = newChartInstance;
    }
  }, [chartData]);

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-6">Dashboard</h2>
      <p className="text-gray-600 mb-4">Select options from the dropdown to get started.</p>
      <Select
        isMulti
        options={stockOptions}
        value={selectedOptions}
        onChange={(value) => setSelectedOptions(value)}
        className="mb-4" 
      />
      <canvas id="chart" height="400" width="800"/>
    </div>
  );
};

export default Dashboard;