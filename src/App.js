import React from "react";
import axios from "axios";

function App() {
  const handleAction = (action) => {
    axios.post("http://127.0.0.1:5000/control", { action })
      .then((response) => console.log(response.data))
      .catch((err) => console.error(err));
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Drowsiness Detection</h1>
      <img
        src="http://127.0.0.1:5000/video_feed"
        alt="Video Feed"
        width="640"
        height="480"
        style={{ border: "2px solid black", borderRadius: "10px" }}
      />
      <div style={{ marginTop: "20px" }}>
        <button onClick={() => handleAction("pause")}>Pause</button>
        <button onClick={() => handleAction("resume")}>Resume</button>
        <button onClick={() => handleAction("stop")}>Stop</button>
      </div>
    </div>
  );
}

export default App;
