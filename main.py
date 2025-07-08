import tkinter as tk
from tkinter import messagebox
import subprocess
import time
import keyboard
import threading
import face_recognition
import cv2

# 📥 Tanınacak yüz verisi
known_image = face_recognition.load_image_file(
    r"C:\Users\ALI RIZA SAHIN\PycharmProjects\pythonProject21\ali_riza.jpg"
)
known_encodings = face_recognition.face_encodings(known_image)
if not known_encodings:
    print("❌ 'ali_riza.jpg' dosyasında yüz bulunamadı.")
    exit()
known_face_encoding = known_encodings[0]

# ❌ Pencereyi kapatma girişimi: onay sor
def on_close():
    cevap = messagebox.askyesno(
        "Çıkmak üzeresiniz",
        "Bu ekranı kapatırsanız bilgisayar kapatılacak. Emin misiniz?"
    )
    if cevap:
        print("❌ Çarpıya basıldı ve onaylandı. Bilgisayar kapatılıyor...")
        subprocess.call("shutdown /s /t 0", shell=True)

# 🧠 Yüz tanıma
def yuz_tanima(root):
    print("📸 Kamera başlatılıyor...")
    cap = cv2.VideoCapture(0)
    access_granted = False
    timeout = time.time() + 15  # 15 saniye içinde yüz tanınmalı

    while time.time() < timeout:
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations:
            encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            for face_encoding in encodings:
                match = face_recognition.compare_faces(
                    [known_face_encoding], face_encoding, tolerance=0.45
                )
                if True in match:
                    access_granted = True
                    break
        if access_granted:
            print("✅ Yüz tanındı. Giriş izni verildi.")
            break

    cap.release()
    if access_granted:
        root.after(0, root.destroy)
    else:
        print("🔴 Yüz tanınmadı. Bilgisayar kapatılıyor...")
        root.after(0, lambda: subprocess.call("shutdown /s /t 0", shell=True))

# ⌨️ Tuş kombinasyonu dinleyici
def kombinasyon_dinle(root, timeout=30):
    print(f"⌛ {timeout} saniye içinde CTRL + SHIFT + CAPSLOCK kombinasyonuna basılmalı...")
    end_time = time.time() + timeout
    while time.time() < end_time:
        if (keyboard.is_pressed('ctrl') and
            keyboard.is_pressed('shift') and
            keyboard.is_pressed('caps lock')):
            print("🟢 Tuş kombinasyonu algılandı.")
            yuz_tanima(root)
            return
        time.sleep(0.1)
    print("🔴 Tuş kombinasyonu algılanmadı. Bilgisayar kapatılıyor...")
    root.after(0, lambda: subprocess.call("shutdown /s /t 0", shell=True))

# ⛔ Ctrl+Esc dinleyici (güvenlik için)
def ctrl_esc_dinle():
    print("🔒 Ctrl+Esc dinleniyor...")
    while True:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('esc'):
            print("❌ Ctrl+Esc algılandı. Bilgisayar kapatılıyor...")
            subprocess.call("shutdown /s /t 0", shell=True)
            break
        time.sleep(0.1)

# 🖥️ Tam ekran GUI
root = tk.Tk()
root.title("Erişim Kısıtlandı")
root.configure(bg='black')
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.protocol("WM_DELETE_WINDOW", on_close)

# 🔁 Kombinasyon kontrolü başlat
threading.Thread(target=kombinasyon_dinle, args=(root,), daemon=True).start()
# 🔁 Ctrl+Esc kombinasyonu için ek dinleyici başlat
threading.Thread(target=ctrl_esc_dinle, daemon=True).start()

# ▶️ Başlat
root.mainloop()
