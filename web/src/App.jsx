import { useState, useEffect } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);


function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/history/")
      .then((res) => res.json())
      .then((data) => setHistory(data))
      .catch((err) => console.error(err));
  }, []);






  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file");
      return;
    }


    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error("Server error");
      }
      const data = await response.json();
      setResult(data);
      setError("");
    } catch (err) {
      console.error("Upload error:", err);
      setError("Upload failed");
    }
  };
  
  const chartData = result
    ? {
      labels: Object.keys(result.summary.equipment_type_distribution),
      datasets: [
        {
          label: "Equipment Count",
          data: Object.values(
            result.summary.equipment_type_distribution
          ),
          backgroundColor: "rgba(75, 192, 192, 0.6)",
        },
      ],
    }
    : null;
    const [hover, setHover] = useState(false);
  return (
  <div
    style={{
      minHeight: "100vh",
      width: "100%",
      background: "#181818",
      color: "white",
      padding: "40px 16px",
    }}
  >
   
    <div
      style={{
        maxWidth: "1100px",
        margin: "0 auto",  
      }}
    >
    
      <h1 style={{ textAlign: "center", marginBottom: "30px" }}>
        Chemical Equipment Visualizer
      </h1>

      
      <div
        style={{
          background: "#2c2929",
          borderRadius: "10px",
          padding: "20px",
          display: "flex",
          flexWrap: "wrap",
          gap: "12px",
          justifyContent: "center",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />
        
        <button onMouseEnter={() => setHover(true)}
  onMouseLeave={() => setHover(false)}
          onClick={handleUpload}
          style={{
            background: hover ? "#1e40af" : "#2563eb",
    color: "white",
    padding: "8px 18px",
    borderRadius: "6px",
    border: "none",
    cursor: "pointer",
          }}
        >
          Upload CSV
        </button>
      </div>

     
      {result && (
        <>
          <div
            style={{
              background: "#2a2a2a",
              borderRadius: "10px",
              padding: "16px",
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
              gap: "16px",
              marginBottom: "30px",
            }}
          >
            <div>Total Equipment:<b> {result.summary.total_equipment}</b></div>
            <div>Avg Flowrate: <b>{result.summary.avg_flowrate.toFixed(2)}</b></div>
            <div>Avg Pressure: <b>{result.summary.avg_pressure.toFixed(2)}</b></div>
            <div>
              Avg Temperature:<b>{" "}
              {result.summary.avg_temperature.toFixed(2)}</b>
            </div>
          </div>

          <div
            style={{
              background: "#343333",
              borderRadius: "10px",
              padding: "20px",
            }}
          >
            <h2 style={{ textAlign: "center", marginBottom: "20px" }}>
              Equipment Type Distribution
            </h2>
            <Bar data={chartData} />
          </div>
        </>
      )}
    </div>
  </div>
);


}

export default App;