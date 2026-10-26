import cv2
import numpy as np

print("=== PILIH SUMBER VIDEO KALIBRASI ===")
print("1. Kamera DroidCam (Live)")
print("2. File Video Basket (Local)")
pilihan = input("Masukkan angka (1 atau 2): ")

if pilihan == '1':
    VIDEO_URL = "http://192.168.0.136:4747/video"
else:
    # PASTIKAN nama file video ini sama persis dengan yang ada di folder komputermu
    # Contoh: "video_basket.mp4"
    VIDEO_URL = "video_basket.mp4" 

points = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        print(f"Titik tersimpan: [{x}, {y}]")
        cv2.circle(img, (x,y), 5, (0,0,255), -1)
        cv2.imshow('Kalibrasi Lapangan', img)

print("\nMenarik 1 frame gambar untuk kalibrasi...")
cap = cv2.VideoCapture(VIDEO_URL)
ret, img = cap.read()
cap.release()

if not ret:
    print("❌ Gagal mengambil gambar. Periksa koneksi DroidCam atau pastikan nama file video benar!")
else:
    print("✅ Gambar berhasil diambil!")
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
