import React, { useEffect, useState } from "react";
import axios from "axios";

const VideoDetections = ({ filename }) => {
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!filename) return;
    axios
      .get(`http://127.0.0.1:8000/detections/${filename}`)
      .then((response) => {
        console.log("API Response:", response.data);
        setDetections(response.data.detections);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching detections:", error);
        setError(error.message);
        setLoading(false);
      });
  }, [filename]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Video Detections</h2>
      <ul>
        {detections.map((det, index) => (
          <li key={index}>
            <strong>ID:</strong> {det.id}, <strong>Confidence:</strong> {det.confidence.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VideoDetections;
