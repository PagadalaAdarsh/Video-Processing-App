import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

const VideoPlayer = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState("");
  const [detections, setDetections] = useState([]);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [videoLoaded, setVideoLoaded] = useState(false); // Track metadata

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (response.data.file_path) {
        const filename = selectedFile.name;
        setVideoUrl(`http://127.0.0.1:8000/video/${filename}`);
        fetchDetections(filename);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const fetchDetections = async (filename) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/detections/${filename}`);
      setDetections(response.data.detections);
    } catch (error) {
      console.error("Error fetching detections:", error);
    }
  };

  const drawBoundingBoxes = () => {
    if (!videoRef.current || !canvasRef.current || !videoLoaded) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (detections.length === 0) return;

    const frameNumber = Math.floor(video.currentTime * 30); // Assuming 30 FPS

    const currentDetections = detections.filter((det) => det.frame_number === frameNumber);

    currentDetections.forEach((det) => {
      ctx.strokeStyle = "lime";
      ctx.lineWidth = 2;
      ctx.strokeRect(det.x1, det.y1, det.x2 - det.x1, det.y2 - det.y1);

      ctx.fillStyle = "red";
      ctx.font = "16px Arial";
      ctx.fillText(`Person ${det.confidence.toFixed(2)}`, det.x1, det.y1 - 5);
    });
  };

  useEffect(() => {
    const interval = setInterval(drawBoundingBoxes, 100);
    return () => clearInterval(interval);
  }, [detections, videoLoaded]);

  return (
    <div>
      <h2>Upload Video</h2>
      <input type="file" accept="video/mp4" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>

      {videoUrl && (
        <div style={{ position: "relative", width: "600px" }}>
          <video
            ref={videoRef}
            controls
            width="600"
            onTimeUpdate={drawBoundingBoxes}
            onLoadedMetadata={() => setVideoLoaded(true)} // Ensure metadata is loaded
          >
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <canvas
            ref={canvasRef}
            style={{ position: "absolute", top: 0, left: 0, pointerEvents: "none" }}
          />
        </div>
      )}
    </div>
  );
};

export default VideoPlayer;
