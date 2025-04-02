import React from "react";
import VideoPlayer from "./api/VideoPlayer";
import VideoDetections from "./api/VideoDetections";

function App() {
  return (
    <div>
      <h1>Object Detection Dashboard</h1>
      <VideoPlayer />
      <VideoDetections />
    </div>
  );
}

export default App;
