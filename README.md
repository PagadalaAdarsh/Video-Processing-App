# Video Processing App

This project is a **FastAPI-based backend** with a **React frontend** for processing videos. The backend handles video uploads, processing, and retrieval, while the frontend provides a UI for interaction.

## Features
- **Upload Videos**: Users can upload video files.
- **Process Videos**: Simulated video processing with frame-by-frame logging.
- **Retrieve Processed Videos**: Fetch and view uploaded videos.
- **Fetch Detections**: Retrieve object detection results from the database.
- **Cleanup**: Delete all uploaded videos.

## Tech Stack
### Backend
- **FastAPI**: Web framework for API development.
- **MySQL**: Database for storing detections.
- **Python-dotenv**: Manage environment variables.
- **CORS Middleware**: Allows cross-origin requests.
- **Docker (optional)**: Deployment.

### Frontend
- **React.js**: UI development.
- **Vite**: Fast development environment.
- **Tailwind CSS (optional)**: Styling.

## Setup Instructions
### 1. Clone the Repository
```sh
git clone https://github.com/PagadalaAdarsh/Video-Processing-App.git
cd Video-Processing-App
```

### 2. Backend Setup
#### Install dependencies
```sh
cd backend
pip install -r requirements.txt
```
#### Configure Environment Variables
Create a `.env` file in the `backend` directory:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=video_processing
```
#### Run Backend Server
```sh
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend Setup
#### Install dependencies
```sh
cd frontend
npm install
```
#### Run Frontend Server
```sh
npm run dev
```
If port `5173` is busy, another port will be assigned.

## API Endpoints
### Root
- `GET /` - Welcome message.

### Video Upload & Processing
- `POST /upload/` - Uploads a video.
- `POST /process/{video_id}` - Simulates video processing.

### Video Retrieval
- `GET /videos/` - Lists uploaded videos.
- `GET /video/{filename}` - Fetches a specific video.

### Detections
- `GET /detections/{video_id}` - Fetches detections from the database.

### Cleanup
- `DELETE /cleanup/` - Deletes all uploaded videos
