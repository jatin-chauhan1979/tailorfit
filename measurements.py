import cv2
import mediapipe as mp
import numpy as np

from fit_adjustment import apply_fit
from garment_measurements import garment_measurements

mp_pose = mp.solutions.pose

def get_measurements(image_path, real_height_cm, garment,fit):
    image = cv2.imread(image_path)
    h, w, _ = image.shape

    with mp_pose.Pose(static_image_mode=True) as pose:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        if not result.pose_landmarks:
            return None

        #landmarks = result.pose_landmarks.landmark
        lm = result.pose_landmarks.landmark

        def pt(i):
            return np.array([lm[i].x * w, lm[i].y * h])

        landmarks = {
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

        body_height_px = np.linalg.norm(
            landmarks["nose"] - (landmarks["left_ankle"] + landmarks["right_ankle"]) / 2
        )
        scale = real_height_cm / body_height_px

        base = garment_measurements(landmarks, scale, garment,fit)
        final = apply_fit(base, fit)

        final["fit_type"] = fit
        final["height_cm"] = real_height_cm

        return final



        return garment_measurements(landmarks, scale, garment)

        def point(idx):
            return np.array([landmarks[idx].x * w,
                             landmarks[idx].y * h])

        # Key Points
        left_shoulder = point(11)
        right_shoulder = point(12)
        left_hip = point(23)
        right_hip = point(24)
        left_ankle = point(27)
        right_ankle = point(28)
        nose = point(0)

        # Pixel calculations
        shoulder_width_px = np.linalg.norm(left_shoulder - right_shoulder)
        hip_width_px = np.linalg.norm(left_hip - right_hip)
        body_height_px = np.linalg.norm(nose - ((left_ankle + right_ankle) / 2))

        # Scale factor
        scale = real_height_cm / body_height_px

        measurements = {
            "shoulder_width_cm": round(shoulder_width_px * scale, 1),
            "chest_estimate_cm": round(shoulder_width_px * scale * 1.35, 1),
            "waist_estimate_cm": round(hip_width_px * scale * 1.25, 1),
            "hip_width_cm": round(hip_width_px * scale, 1),
            "height_cm": real_height_cm
        }

        return measurements

def garment_measurementsOld(landmarks, scale, garment):
    def dist(p1, p2):
        return np.linalg.norm(p1 - p2) * scale

    left_shoulder = landmarks["left_shoulder"]
    right_shoulder = landmarks["right_shoulder"]
    left_hip = landmarks["left_hip"]
    right_hip = landmarks["right_hip"]
    left_elbow = landmarks["left_elbow"]
    left_wrist = landmarks["left_wrist"]

    output = {}

    # COMMON
    output["shoulder"] = round(dist(left_shoulder, right_shoulder), 1)

    if garment == "shirt":
        output.update({
            "chest": round(output["shoulder"] * 1.35, 1),
            "waist": round(dist(left_hip, right_hip) * 1.25, 1),
            "sleeve_length": round(dist(left_shoulder, left_wrist), 1),
            "shirt_length": round(dist(left_shoulder, left_hip) * 1.15, 1)
        })

    elif garment == "tshirt":
        output.update({
            "chest": round(output["shoulder"] * 1.25, 1),
            "length": round(dist(left_shoulder, left_hip), 1),
            "half_sleeve": round(dist(left_shoulder, left_elbow), 1)
        })

    elif garment == "blouse":
        output.update({
            "bust": round(output["shoulder"] * 1.40, 1),
            "under_bust": round(output["shoulder"] * 1.30, 1),
            "blouse_length": round(dist(left_shoulder, left_hip) * 0.65, 1),
            "sleeve_length": round(dist(left_shoulder, left_elbow), 1)
        })

    return output

