import React from "react";

function ControlButtons({ onAction }) {
  return (
    <div className="button-container">
      <button className="btn pause" onClick={() => onAction("pause")}>
        Pause
      </button>
      <button className="btn resume" onClick={() => onAction("resume")}>
        Resume
      </button>
      <button className="btn stop" onClick={() => onAction("stop")}>
        Stop
      </button>
    </div>
  );
}

export default ControlButtons;
