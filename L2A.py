import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print("Gagal membaca kamera")
        continue

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(img_rgb)

    status = " "

    if result.pose_landmarks:
        mp_draw.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        lm = result.pose_landmarks.landmark
    
        left_shoulder = lm[11].y
        right_shoulder = lm[12].y
        left_wrist = lm[15].y
        right_wrist = lm[16].y
        
        tangan_terangkat = (
            left_wrist < left_shoulder or
            right_wrist < right_shoulder
        )

        if tangan_terangkat:
            status = "TANGAN TERANGKAT"
        else:
            status = "TANGAN TIDAK TERANGKAT"

    cv2.putText(img, status, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    cv2.imshow("Deteksi Tangan Terangkat", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
