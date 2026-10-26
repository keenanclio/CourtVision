import cv2
import numpy as np
import json
import asyncio
import websockets
from ultralytics import YOLO

# Load model YOLOv8 nano
model = YOLO('yolov8n.pt') 

# Masukkan kedua sumber videonya
DROIDCAM_URL = "http://192.168.0.136:4747/video"
VIDEO_FILE = "basket.mp4" # Ganti dengan nama file videomu

# ==========================================
# PASTE HASIL KODE KALIBRASI KAMU DI SINI
pts_src = np.array([
    [452, 346],  
    [1265, 374],  
    [1233, 704],  
    [96, 609]     
], dtype=np.float32) 
# ==========================================

# ... (kode ukuran canvas dan matrix tetap sama) ...

async def detect_and_send(websocket):
    print("Mencoba menghubungkan ke DroidCam...")
    cap = cv2.VideoCapture(DROIDCAM_URL)
    
    # Cek apakah DroidCam menyala dan bisa dibaca
    if not cap.isOpened() or not cap.read()[0]:
        print("⚠️ DroidCam tidak terdeteksi atau mati.")
        print("🔄 Otomatis beralih memutar file video lokal...")
        cap = cv2.VideoCapture(VIDEO_FILE)
        sumber_video = "file"
    else:
        print("✅ Berhasil terhubung ke DroidCam secara Live!")
        sumber_video = "live"

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            if sumber_video == "file":
                # Mengulang video otomatis (looping) jika sudah habis
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            else:
                print("⚠️ Kehilangan sinyal DroidCam.")
                break

        # ... (sisa kode deteksi YOLO dan WebSocket ke bawahnya tetap sama persis) ...
