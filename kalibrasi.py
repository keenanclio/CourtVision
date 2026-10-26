import cv2
import numpy as np

# Gunakan IP yang sama dengan tracker
VIDEO_URL = "http://192.168.0.136:4747/video"
points = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        print(f"Titik tersimpan: [{x}, {y}]")
        cv2.circle(img, (x,y), 5, (0,0,255), -1)
        cv2.imshow('Kalibrasi Lapangan', img)

print("Menarik 1 frame gambar dari kamera untuk kalibrasi...")
cap = cv2.VideoCapture(VIDEO_URL)
ret, img = cap.read()
cap.release()

if not ret:
    print("❌ Gagal mengambil gambar dari kamera. Periksa koneksi DroidCam!")
else:
    print("\n✅ Gambar berhasil diambil!")
    print("KLIK 4 SUDUT LAPANGAN SECARA BERURUTAN:")
    print("1. Kiri Atas  2. Kanan Atas  3. Kanan Bawah  4. Kiri Bawah")
    
    cv2.imshow('Kalibrasi Lapangan', img)
    cv2.setMouseCallback('Kalibrasi Lapangan', click_event)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    if len(points) == 4:
        print("\n=== COPY KODE DI BAWAH INI KE tracker.py ===")
        print(f"pts_src = np.array({points}, dtype=np.float32)")
        print("============================================")
    else:
        print("\n⚠️ Kamu belum mengklik genap 4 titik!")