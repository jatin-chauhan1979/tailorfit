import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose

def detect_landmarks(image_path):
    image = cv2.imread(image_path)
    h, w, _ = image.shape

    with mp_pose.Pose(static_image_mode=True) as pose:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        if not result.pose_landmarks:
            return None

        lm = result.pose_landmarks.landmark

        def pt(i):
            return np.array([lm[i].x * w, lm[i].y * h])

        return {
            "left_shoulder": pt(11),
            "right_shoulder": pt(12),
            "left_elbow": pt(13),
            "left_wrist": pt(15),
            "left_hip": pt(23),
            "right_hip": pt(24),
            "left_ankle": pt(27),
            "right_ankle": pt(28),
            "nose": pt(0)
        }
