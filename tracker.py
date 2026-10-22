import cv2
import numpy as np
import json
import asyncio
import websockets
from ultralytics import YOLO

# 1. Load Model AI
model = YOLO('yolov8n.pt') 

# MASUKKAN IP DROIDCAM KAMU DI SINI
VIDEO_SOURCE = "http://192.168.0.136:4747/video" 

# ==========================================
# KONFIGURASI HOMOGRAPHY (BIRD'S-EYE VIEW)
# ==========================================

# A. 4 Titik Sudut di Video Asli (Kamera HP)
# URUTAN HARUS: Kiri-Atas, Kanan-Atas, Kanan-Bawah, Kiri-Bawah
# WAJIB DIGANTI: Sesuaikan angka ini dengan letak sudut lapangan di kameramu
pts_src = np.array([
    [100, 150],  # Titik 1: Sudut Kiri Atas di video
    [540, 150],  # Titik 2: Sudut Kanan Atas di video
    [640, 480],  # Titik 3: Sudut Kanan Bawah di video
    [0, 480]     # Titik 4: Sudut Kiri Bawah di video
], dtype=float)

# B. 4 Titik Sudut yang Bersesuaian di Canvas HTML (Ukuran 800x450)
# Ini adalah batas garis luar lapangan (margin 20px yang kita buat di JavaScript)
margin = 20
canvas_w = 800
canvas_h = 450
pts_dst = np.array([
    [margin, margin],                       # Titik 1: Kiri Atas 
    [canvas_w - margin, margin],            # Titik 2: Kanan Atas
    [canvas_w - margin, canvas_h - margin], # Titik 3: Kanan Bawah
    [margin, canvas_h - margin]             # Titik 4: Kiri Bawah
], dtype=float)

# C. Hitung Matriks Transformasi
matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

# ==========================================

async def detect_and_send(websocket):
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # AI mendeteksi manusia
        results = model(frame, classes=[0], verbose=False)
        players_data = []
        
        for r in results:
            for box in r.boxes:
                # Dapatkan kotak objek
                x1, y1, x2, y2 = box.xyxy[0]
                
                # Ambil titik pusat kaki pemain
                px = float((x1 + x2) / 2)
                py = float(y2)
                
                # TRANSFORMASI HOMOGRAPHY: Ubah (px, py) miring menjadi lurus (2D)
                # OpenCV butuh format array 3D: [[[x, y]]]
                point_original = np.array([[[px, py]]], dtype=float)
                point_transformed = cv2.perspectiveTransform(point_original, matrix)
                
                # Ekstrak hasil koordinat X dan Y yang sudah berformat Bird's-Eye
                map_x = int(point_transformed[0][0][0])
                map_y = int(point_transformed[0][0][1])
                
                players_data.append({"x": map_x, "y": map_y})

        # --- VISUALISASI DI LAYAR PYTHON ---
        # Gambar garis hijau kotak Homography di layar video untuk membantu kalibrasi
        cv2.polylines(frame, [np.int32(pts_src)], True, (0, 255, 0), 2)
        
        # Kirim data ke Web HTML
        try:
            await websocket.send(json.dumps(players_data))
        except:
            break 

        cv2.imshow("AI Vision - Homography (Tekan 'q' untuk keluar)", frame)
        if cv2.waitKey(1) == ord('q'):
            break
            
        await asyncio.sleep(0.03) 
        
    cap.release()
    cv2.destroyAllWindows()

async def main():
    print("Mempersiapkan AI dengan Homography...")
    async with websockets.serve(detect_and_send, "localhost", 8765):
        print("✅ Server AI siap! Buka index.html di browser.")
        await asyncio.Future() 

asyncio.run(main())
