import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
from collections import deque
import time
import threading
import os
import pygame
from scipy.io.wavfile import write  # For generating alarm sound
import numpy as np


class DrowsinessDetector:
    def __init__(self):
        # Load pre-trained models
        self.eye_model = tf.keras.models.load_model(
            r"C:\Users\dell\drowsy-web\training\eye_model.h5"
        )
        self.yawn_model = tf.keras.models.load_model(
            r"C:\Users\dell\drowsy-web\training\yawn_model.h5"
        )

        # MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

        # Rolling windows for predictions
        self.eye_history = deque(maxlen=5)
        self.yawn_history = deque(maxlen=5)

        # Video capture
        self.cap = cv2.VideoCapture(0)

        # States
        self.closed_frames = 0
        self.yawn_frames = 0
        self.is_drowsy = False

        # Control flags
        self.paused = False
        self.stopped = False

        # Alarm state
        self.alarm_on = False
        self.alarm_file = os.path.join(os.getcwd(), "alarm.wav")

        # Ensure alarm file exists
        self.ensure_alarm_file()

    def ensure_alarm_file(self):
        """Generate a simple alarm.wav if it doesn't exist."""
        if not os.path.exists(self.alarm_file):
            print("No alarm file found. Generating 'alarm.wav'...")
            duration = 2  # seconds
            frequency = 440  # Hz
            sample_rate = 44100

            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
            waveform_integers = np.int16(waveform * 32767)

            write(self.alarm_file, sample_rate, waveform_integers)
            print("Generated alarm.wav!")

    def play_alarm(self):
        """Play alarm using pygame (non-blocking)."""
        if not self.alarm_on:
            self.alarm_on = True
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(self.alarm_file)
                pygame.mixer.music.play()
                print("Alarm playing...")
            except Exception as e:
                print(f"Alarm sound failed: {e}")
            finally:
                self.alarm_on = False

    def preprocess_img(self, img, target_size=(64, 64)):
        img = cv2.resize(img, target_size)
        img = img / 255.0
        return np.expand_dims(img, axis=0)

    def generate_frames(self):
        """Yield frames for Flask video feed."""
        while not self.stopped:
            if self.paused:
                time.sleep(0.1)
                continue

            ret, frame = self.cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)

            final_eye_state = "Unknown"
            final_yawn_state = "Unknown"

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    h, w, _ = frame.shape

                    # Eye detection
                    left_eye_points = [33, 133, 160, 159, 158, 153, 144, 145]
                    eye_coords = [(int(face_landmarks.landmark[i].x * w),
                                   int(face_landmarks.landmark[i].y * h)) for i in left_eye_points]
                    x_min = max(min([p[0] for p in eye_coords]) - 5, 0)
                    x_max = min(max([p[0] for p in eye_coords]) + 5, w)
                    y_min = max(min([p[1] for p in eye_coords]) - 5, 0)
                    y_max = min(max([p[1] for p in eye_coords]) + 5, h)
                    eye_crop = frame[y_min:y_max, x_min:x_max]

                    if eye_crop.size > 0:
                        eye_pred = self.eye_model.predict(self.preprocess_img(eye_crop), verbose=0)
                        eye_state = "Closed" if eye_pred[0][0] > 0.5 else "Open"
                        self.eye_history.append(eye_state)
                        final_eye_state = max(set(self.eye_history), key=self.eye_history.count)
                        self.closed_frames = self.closed_frames + 1 if final_eye_state == "Closed" else 0
                        cv2.putText(frame, f"Eye: {final_eye_state}", (30, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                    # Mouth detection
                    mouth_points = [61, 291, 78, 308, 13, 14, 87, 317]
                    mouth_coords = [(int(face_landmarks.landmark[i].x * w),
                                     int(face_landmarks.landmark[i].y * h)) for i in mouth_points]
                    mx_min = max(min([p[0] for p in mouth_coords]) - 5, 0)
                    mx_max = min(max([p[0] for p in mouth_coords]) + 5, w)
                    my_min = max(min([p[1] for p in mouth_coords]) - 5, 0)
                    my_max = min(max([p[1] for p in mouth_coords]) + 5, h)
                    mouth_crop = frame[my_min:my_max, mx_min:mx_max]

                    if mouth_crop.size > 0:
                        yawn_pred = self.yawn_model.predict(self.preprocess_img(mouth_crop), verbose=0)
                        yawn_state = "Yawning" if yawn_pred[0][0] > 0.5 else "No Yawn"
                        self.yawn_history.append(yawn_state)
                        final_yawn_state = max(set(self.yawn_history), key=self.yawn_history.count)
                        self.yawn_frames = self.yawn_frames + 1 if final_yawn_state == "Yawning" else 0
                        cv2.putText(frame, f"Mouth: {final_yawn_state}", (30, 90),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Drowsiness check
            if self.closed_frames > 15 or self.yawn_frames > 15:
                self.is_drowsy = True
                cv2.putText(frame, "DROWSY ALERT!", (100, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                threading.Thread(target=self.play_alarm, daemon=True).start()
            else:
                self.is_drowsy = False

            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        self.cap.release()

    # Control functions
    def pause(self):
        print("Video paused.")
        self.paused = True

    def resume(self):
        print("Video resumed.")
        self.paused = False

    def stop(self):
        print("Video stopped.")
        self.stopped = True
        self.cap.release()
