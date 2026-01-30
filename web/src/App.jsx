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
  const cardStyle = {
    background: "#414040",
    padding: "20px",
    borderRadius: "8px",
    flex: "1 1 200px",
    textAlign: "center",
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
  return (
    <div style={{ padding: '10%', display: 'grid' }}>
      <h1>Chemical Equipment Visualizer</h1>


      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      /><br></br>



      <button onClick={handleUpload}>Upload CSV</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {history.length > 0 && (
        <div style={{ marginTop: "20px", display: "flex", flexDirection: "column", gap: "10px" }}>
          <label>Select Previous Dataset: </label>
          <select style={{ padding: "8px", maxWidth: "300px" }}
            onChange={(e) => {
              const id = e.target.value;
              fetch(`http://127.0.0.1:8000/api/summary/${id}/`)
                .then((res) => res.json())
                .then((data) => setResult(data));
            }}
          >
            <option value="">-- Select --</option>
            {history.map((item) => (
              <option key={item.dataset_id} value={item.dataset_id}>
                {item.file_name} ({item.dataset_id})
              </option>
            ))}
          </select>
        </div>
      )}
      {result && (
        <div style={{ display: 'grid' }}>
          <h2>Summary</h2>

          <div style={{
            display: "flex", gap: "20px", flexWrap: "wrap",
            justifyContent: "space-between",
          }}>
            <div style={cardStyle}>
              <h3>Total Equipment</h3>
              <p>{result.summary.total_equipment}</p>
            </div>

            <div style={cardStyle}>
              <h3>Avg Flowrate</h3>
              <p>{result.summary.avg_flowrate.toFixed(2)}</p>
            </div>

            <div style={cardStyle}>
              <h3>Avg Pressure</h3>
              <p>{result.summary.avg_pressure.toFixed(2)}</p>
            </div>

            <div style={cardStyle}>
              <h3>Avg Temperature</h3>
              <p>{result.summary.avg_temperature.toFixed(2)}</p>
            </div>
          </div>
          {chartData && (
            <div style={{ marginTop: "40px", maxWidth: "800px", width: "100%", }}>
              <h2>Equipment Type Distribution</h2>
              <Bar data={chartData} />
            </div>
          )}

        </div>
      )}
    </div>
  );
}

export default App;