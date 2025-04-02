from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MySQL using environment variables
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

@app.get("/")  
def home():
    return {"message": "Welcome to the Video Processing API"}

@app.get("/detections")
def get_detections():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detections ORDER BY timestamp DESC")
    detections = cursor.fetchall()
    cursor.close()
    return {"detections": detections}
