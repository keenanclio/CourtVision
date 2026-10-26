import cv2
import numpy as np
import json
import asyncio
import websockets
from ultralytics import YOLO

# Load model YOLOv8 nano (ringan dan cepat untuk real-time)
model = YOLO('yolov8n.pt') 

# Ganti IP di bawah ini SESUAI dengan IP DroidCam di HP kamu (cukup ubah di sini saja)
VIDEO_URL = "http://192.168.0.136:4747/video" 

# ==========================================
# PASTE HASIL KODE KALIBRASI KAMU DI SINI
pts_src = np.array([
    [452, 346],  
    [1265, 374],  
    [1233, 704],  
    [96, 609]     
], dtype=np.float32) 
# ==========================================

canvas_w = 800
canvas_h = 450
margin = 20
pts_dst = np.array([
    [margin, margin],
    [canvas_w - margin, margin],
    [canvas_w - margin, canvas_h - margin],
    [margin, canvas_h - margin]
], dtype=np.float32) 

# Matriks transformasi perspektif dari kamera ke map 2D
matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

# Fungsi mendeteksi warna baju (HSV)
def deteksi_tim(frame, x1, y1, x2, y2):
    try:
        h = int(y2 - y1)
        w = int(x2 - x1)
        # Ambil area dada/badan bagian atas pemain
        baju = frame[int(y1):int(y1 + h/2), int(x1):int(x2)]
        
        hsv = cv2.cvtColor(baju, cv2.COLOR_BGR2HSV)
        
        # Rentang warna Biru (Tim A)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        if cv2.countNonZero(mask_blue) > (h * w * 0.1): 
            return "TimBiru"
        else:
            return "TimKuning" # Sisanya dianggap Tim B / Kuning
    except:
        return "TimKuning"

async def detect_and_send(websocket):
    print("Menghubungkan ke kamera DroidCam...")
    cap = cv2.VideoCapture(VIDEO_URL)
    
    if not cap.isOpened():
        print("❌ Gagal terhubung ke kamera! Periksa kembali URL atau jaringan WiFi.")
        return

    print("✅ Berhasil terhubung ke kamera! Streaming berjalan...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Kehilangan sinyal video dari kamera.")
            break

        # Deteksi manusia menggunakan YOLOv8 (classes=[0] khusus untuk 'person')
        results = model(frame, classes=[0], verbose=False)
        players_data = []
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                
                # Cek warna tim berdasarkan baju
                tim = deteksi_tim(frame, x1, y1, x2, y2)
                
                # Titik tumpuan kaki pemain di lapangan (tengah bawah bounding box)
                px = float((x1 + x2) / 2)
                py = float(y2)
                
                point_original = np.array([[[px, py]]], dtype=np.float32)
                point_transformed = cv2.perspectiveTransform(point_original, matrix)
                
                map_x = int(point_transformed[0][0][0])
                map_y = int(point_transformed[0][0][1])
                
                # Kirim data jika posisi berada di dalam batas kanvas
                if -50 <= map_x <= 850 and -50 <= map_y <= 500:
                    players_data.append({"x": map_x, "y": map_y, "team": tim})

        # Gambar garis kalibrasi di video asli sebagai referensi
        cv2.polylines(frame, [np.int32(pts_src)], True, (0, 255, 0), 2)
        
        try:
            await websocket.send(json.dumps(players_data))
        except websockets.exceptions.ConnectionClosed:
            print("⚠️ Koneksi WebSocket dengan browser terputus.")
            break

        cv2.imshow("AI Vision - Tracker (Tekan 'q' untuk keluar)", frame)
        if cv2.waitKey(1) == ord('q'):
            break
            
        await asyncio.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()

async def main():
    async with websockets.serve(detect_and_send, "localhost", 8765):
        print("✅ Server AI & WebSocket aktif di ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
