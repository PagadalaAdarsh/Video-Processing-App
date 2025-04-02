from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import mysql.connector

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="adarsh9014046027",
        database="video_processing"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")
    cursor = None  # Prevent usage of an uninitialized cursor

# Directory to store uploaded videos
UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Root Endpoint (Fixes 404 issue)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Video Processing API"}

# ✅ Video Upload Endpoint
@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith((".mp4", ".avi", ".mkv", ".mov")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a video file.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Video uploaded successfully!", "filename": file.filename, "file_path": file_path}

# ✅ Video Processing Endpoint
@app.post("/process/{video_id}")
async def process_video(video_id: str):
    file_path = os.path.join(UPLOAD_DIR, video_id)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Video not found")

    # Simulate video processing
    return {"message": "Processing video...", "video_id": video_id, "file_path": file_path}

# ✅ List Uploaded Videos
@app.get("/videos/")
async def list_videos():
    videos = os.listdir(UPLOAD_DIR)
    return {"uploaded_videos": videos}

# ✅ Get Specific Video
@app.get("/video/{filename}")
async def get_video(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(file_path, media_type="video/mp4")

# ✅ Fetch Detections for a Given Video
@app.get("/detections/{video_id}")
async def get_detections(video_id: str):
    if cursor is None:
        raise HTTPException(status_code=500, detail="Database connection is not available")

    try:
        query = "SELECT id, frame_number, timestamp, x1, y1, x2, y2, confidence FROM detections WHERE frame_number IS NOT NULL"
        cursor.execute(query)
        results = cursor.fetchall()

        detections = [
            {
                "id": row[0],
                "frame_number": row[1],
                "timestamp": row[2],
                "x1": row[3],
                "y1": row[4],
                "x2": row[5],
                "y2": row[6],
                "confidence": row[7]
            }
            for row in results
        ]

        return {"detections": detections}

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
        raise HTTPException(status_code=500, detail="Database query failed")


# ✅ Cleanup Endpoint (Optional)
@app.delete("/cleanup/")
async def cleanup():
    """ Deletes all uploaded videos. Use with caution! """
    try:
        for file in os.listdir(UPLOAD_DIR):
            os.remove(os.path.join(UPLOAD_DIR, file))
        return {"message": "All uploaded videos have been deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {e}")
