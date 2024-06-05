import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import Select from "react-select";

const options = [
  { value: "IBM", label: "IBM" },
  { value: "TSCO.LON", label: "TSCO.LON" },
  { value: "SHOP.TRT", label: "SHOP.TRT" },
  { value: "GPV.TRV", label: "GPV.TRV" },
  { value: "MBG.DEX", label: "MBG.DEX" },
  { value: "RELIANCE.BSE", label: "RELIANCE.BSE" },
  { value: "600104.SHH", label: "600104.SHH" },
  { value: "000002.SHZ", label: "000002.SHZ" },
];

const Dashboard = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [chartData, setChartData] = useState({});

  useEffect(() => {
    if (selectedOptions.length > 0) {
      const fetchData = async () => {
        try {
          const responses = await Promise.all(
            selectedOptions.map((option) =>
              fetch(
                `http://localhost:3000/load_data?symbol=${option.value}`
              ).then((response) => {
                if (!response.ok) {
                  throw new Error("Network response was not ok");
                }
                return response.json();
              })
            )
          );
          const dataSets = responses.map((data, index) => ({
            label: selectedOptions[index].label,
            data: Object.entries(data).map(([date, close]) => ({
              x: date,
              y: parseFloat(close),
            })),
            borderColor: `#${Math.floor(Math.random() * 16777215).toString(
              16
            )}`,
            fill: false,
          }));
          setChartData({
            datasets: dataSets,
          });
        } catch (error) {
          console.error("Failed to fetch data:", error);
        }
      };
      fetchData();
    } else {
      setChartData({});
    }
  }, [selectedOptions]);

  return (
    <div>
      <h2>Main Dashboard Page</h2>
      
    </div>
  );
};

export default Dashboard;
