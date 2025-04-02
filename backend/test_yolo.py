import cv2
import mysql.connector
from ultralytics import YOLO
from datetime import datetime
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env file
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# ✅ Connect to MySQL
try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL successfully!")
except mysql.connector.Error as err:
    print(f"❌ MySQL Connection Error: {err}")
    exit()

# ✅ Load YOLOv8 model
print("Loading YOLO model...")
model = YOLO("yolov8n.pt")  
print("YOLO model loaded successfully!")

# ✅ Open the video file
video_path = "uploaded_videos/tomshelby.mp4"  
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Error: Could not open video.")
    exit()

frame_number = 0  

# ✅ Process video frame by frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  

    frame_number += 1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Run YOLO detection
    results = model(frame)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            conf = float(box.conf[0].item())  
            cls = int(box.cls[0].item())  

            if cls == 0:  # Only store detections for "person"
                print(f"🔹 Detected person: Frame {frame_number}, Confidence {conf:.2f}, Coordinates: ({x1}, {y1}), ({x2}, {y2})")
                try:
                    cursor.execute('''
                        INSERT INTO detections (frame_number, timestamp, x1, y1, x2, y2, confidence)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (frame_number, timestamp, x1, y1, x2, y2, conf))
                    conn.commit()
                    print("✅ Inserted Successfully!")
                except mysql.connector.Error as err:
                    print(f"❌ MySQL Insert Error: {err}")

                # Draw the detection on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  
                cv2.putText(frame, f"Person {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # ✅ Show frame
    cv2.imshow("YOLOv8 Person Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ✅ Release resources
cap.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()

print("Video processing complete. Detections saved to MySQL database.")
