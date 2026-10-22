import cv2
import json
import asyncio
import websockets
from ultralytics import YOLO

# 1. Load Model AI (YOLOv8 nano - versi paling ringan dan cepat)
model = YOLO('yolov8n.pt') 

# GANTI IP INI DENGAN IP DROIDCAM KAMU
VIDEO_SOURCE = "http://192.168.0.136:4747/video" 

async def detect_and_send(websocket):
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    
    # Ambil resolusi asli dari kamera
    cam_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if cam_width == 0: cam_width, cam_height = 640, 480 # Fallback default

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 2. AI Mendeteksi objek (classes=[0] artinya HANYA mendeteksi manusia)
        results = model(frame, classes=[0], verbose=False)
        
        players_data = []
        
        for r in results:
            for box in r.boxes:
                # Koordinat kotak (bounding box) yang mendeteksi pemain
                x1, y1, x2, y2 = box.xyxy[0]
                
                # Kita ambil titik TENGAH BAWAH (kaki pemain) agar akurat di lapangan
                px = int((x1 + x2) / 2)
                py = int(y2)
                
                # 3. Transformasi ke ukuran Canvas HTML kita (800x450)
                # Catatan: Ini transformasi proporsional sederhana. 
                # Untuk Homography murni (Bird's-eye view asli), butuh rumus matriks (cv2.getPerspectiveTransform)
                map_x = int((px / cam_width) * 800)
                map_y = int((py / cam_height) * 450)
                
                players_data.append({"x": map_x, "y": map_y})

        # 4. Kirim data pemain (X dan Y) ke Website HTML
        try:
            await websocket.send(json.dumps(players_data))
        except:
            break # Jika web ditutup, berhenti ngirim

        # (Opsional) Tampilkan layar AI yang sedang bekerja di Python
        cv2.imshow("AI Vision (Tekan 'q' untuk keluar)", frame)
        if cv2.waitKey(1) == ord('q'):
            break
            
        await asyncio.sleep(0.03) # Jeda agar tidak membuat laptop lag
        
    cap.release()
    cv2.destroyAllWindows()

# Menyalakan server WebSocket
async def main():
    print("Mempersiapkan AI...")
    async with websockets.serve(detect_and_send, "localhost", 8765):
        print("✅ Server AI siap! Sekarang buka index.html di browser kamu.")
        await asyncio.Future()  # Biarkan server menyala terus

# Jalankan program
asyncio.run(main())