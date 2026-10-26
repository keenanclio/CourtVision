import cv2
import numpy as np
import json
import asyncio
import websockets
from ultralytics import YOLO

# Load model YOLOv8 nano
model = YOLO('yolov8n.pt') 

# Konfigurasi Sumber Video
DROIDCAM_URL = "http://192.168.0.136:4747/video"
VIDEO_FILE = "basket.mp4" # Pastikan file basket.mp4 ada di folder yang sama

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

matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

def deteksi_tim(frame, x1, y1, x2, y2):
    try:
        h = int(y2 - y1)
        w = int(x2 - x1)
        baju = frame[int(y1):int(y1 + h/3), int(x1):int(x2)] 
        
        hsv = cv2.cvtColor(baju, cv2.COLOR_BGR2HSV)
        
        # Rentang warna biru gelap/navy (untuk tim USA)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([140, 255, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        if cv2.countNonZero(mask_blue) > (h * w * 0.05): 
            return "TimBiru" 
        else:
            return "TimKuning" 
    except:
        return "TimKuning"

async def detect_and_send(websocket):
    print("Mencoba menghubungkan ke DroidCam...")
    cap = cv2.VideoCapture(DROIDCAM_URL)
    
    # Deteksi otomatis sumber video
    if not cap.isOpened() or not cap.read()[0]:
        print("⚠️ DroidCam tidak terdeteksi atau mati.")
        print("🔄 Otomatis beralih memutar file video lokal (basket.mp4)...")
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

        # Filter tinggi bounding box untuk mengabaikan penonton di latar belakang
        results = model(frame, classes=[0], conf=0.4, verbose=False)
        players_data = []
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                
                # Abaikan objek terlalu kecil (kemungkinan besar penonton di tribun)
                if (y2 - y1) < 40:
                    continue
                    
                tim = deteksi_tim(frame, x1, y1, x2, y2)
                
                px = float((x1 + x2) / 2)
                py = float(y2)
                
                point_original = np.array([[[px, py]]], dtype=np.float32)
                point_transformed = cv2.perspectiveTransform(point_original, matrix)
                
                map_x = int(point_transformed[0][0][0])
                map_y = int(point_transformed[0][0][1])
                
                if -50 <= map_x <= 850 and -50 <= map_y <= 500:
                    players_data.append({"x": map_x, "y": map_y, "team": tim})

        cv2.polylines(frame, [np.int32(pts_src)], True, (0, 255, 0), 2)
        
        try:
            await websocket.send(json.dumps(players_data))
        except websockets.exceptions.ConnectionClosed:
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
