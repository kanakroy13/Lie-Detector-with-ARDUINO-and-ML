import cv2
import dlib
import imutils
import numpy as np7q
import matplotlib.pyplot as plt
from collections import deque
from scipy.spatial import distance as dist
from imutils import face_utils

# 🔹 Change Camera Input Here
camera_source = 0  # 0 for default webcam, 1 for external, or "http://your_ip:8080/video" for phone cam

# Load Haar Cascades & Dlib Model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Load Dlib face detector & shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('Model/shape_predictor_68_face_landmarks.dat')

# Eye landmark indexes
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Blink Detection Parameters
blink_threshold = 0.2
frame_success = 2
frame_count = 0
sudden_blink_counter = 0

# Pupil Size Tracking Parameters
PIXELS_PER_MM = 10 
THRESHOLD_CHANGE = 2.2
sudden_pupil_counter = 0
pupil_sizes = deque(maxlen=50)

# Initialize graph
plt.ion()
fig, ax = plt.subplots()
ax.set_title("Pupil Size Over Time")
ax.set_xlabel("Frames")
ax.set_ylabel("Pupil Size (mm)")
(line,) = ax.plot([], [], 'g-')

# Initialize Camera
cap = cv2.VideoCapture(camera_source)

def EAR_calculate(eye):
    a1 = dist.euclidean(eye[1], eye[5])
    a2 = dist.euclidean(eye[2], eye[4])
    m = dist.euclidean(eye[0], eye[3])
    return (a1 + a2) / (2.0 * m)

def eyeLandmark(img, eyes):
    for eye in eyes:
        for i in range(6):
            cv2.circle(img, tuple(eye[i]), 3, (200, 223, 0), -1)
    return img

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        lefteye = shape[L_start:L_end]
        righteye = shape[R_start:R_end]
        avg_EAR = (EAR_calculate(lefteye) + EAR_calculate(righteye)) / 2

        img = frame.copy()
        img = eyeLandmark(img, [lefteye, righteye])

        # Blink Detection Logic
        if avg_EAR < blink_threshold:
            frame_count += 1
        else:
            if frame_count >= frame_success:
                sudden_blink_counter += 1
                cv2.putText(img, 'Blink Detected', (40, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (233, 0, 189), 1)
            frame_count = 0

        # Pupil Detection & Sudden Change Counter
        eyes = eye_cascade.detectMultiScale(gray)
        for (ex, ey, ew, eh) in eyes:
            eye_gray = gray[ey:ey+eh, ex:ex+ew]
            eye_color = frame[ey:ey+eh, ex:ex+ew]

            eye_gray = cv2.equalizeHist(eye_gray)
            blurred = cv2.GaussianBlur(eye_gray, (7, 7), 0)
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if 50 < area < 500:
                    (cx, cy), radius = cv2.minEnclosingCircle(cnt)
                    cx, cy, radius = int(cx), int(cy), int(radius)

                    if 5 < radius < 30:
                        pupil_size_mm = radius / PIXELS_PER_MM
                        pupil_sizes.append(pupil_size_mm)

                        if len(pupil_sizes) > 1:
                            change = abs(pupil_sizes[-1] - pupil_sizes[-2])
                            if change > THRESHOLD_CHANGE:
                                sudden_pupil_counter += 1

                        cv2.circle(eye_color, (cx, cy), radius, (0, 0, 255), 2)
                        cv2.putText(eye_color, f"{pupil_size_mm:.2f} mm", (cx - 20, cy - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        break

    # Display Counters
    cv2.putText(frame, f"Sudden Pupil Changes: {sudden_pupil_counter}", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(frame, f"Sudden Blinks: {sudden_blink_counter}", (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('Pupil & Blink Detection', frame)

    # Update Graph
    ax.clear()
    ax.set_title("Pupil Size Over Time")
    ax.set_xlabel("Frames")
    ax.set_ylabel("Pupil Size (mm)")
    ax.plot(range(len(pupil_sizes)), pupil_sizes, 'g-')
    plt.pause(0.01)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.show()
