import cv2
import mediapipe as mp
from collections import deque

from script3 import imgRGB, total_z, smooth_z

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
z_buffer = deque(maxlen=5)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if reults.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
            img,
            hand_landmarks.landmark,
            mp_hands.HAND_CONNECTIONS,
            )

            total_z = 0
            for lm in hand_landmarks.landmark:
                total_z += lm.z

            avg = total_z / len(hand_landmarks.landmark)

            z_buffer.append(avg)
            smooth_z = sum(z_buffer) / len(z_buffer)

            h, w, c = img.shape
            cx = int(hand_landmarks.landmark[0].x * w)
            cy = int(hand_landmarks.landmark[0].y * w)

            if smooth_z < -0.07:
                posisi = "DEPAN"
                warna = (0, 255, 0)
            else:
                posisi = "BELAKANG"
                warna = (0, 0, 255)

            cv2.putText(img, posisi, (cx - 60, cy - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, warna, 3)

            cv2.putText(img, f"Z: {round(smooth_z, 3)}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cap.inshow("Deteksi Depan & Belakang (Versi Terbaru)", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
