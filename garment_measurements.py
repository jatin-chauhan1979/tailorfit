import numpy as np

from blouse_measurements import blouse_measurements

def garment_measurements(landmarks, scale, garment,fit):
    def dist(p1, p2):
        return np.linalg.norm(p1 - p2) * scale

    shoulder = dist(landmarks["left_shoulder"], landmarks["right_shoulder"])
    hip = dist(landmarks["left_hip"], landmarks["right_hip"])
    leg_length = dist(landmarks["left_hip"], landmarks["left_ankle"])

    left_shoulder = landmarks["left_shoulder"]
    right_shoulder = landmarks["right_shoulder"]
    left_hip = landmarks["left_hip"]
    right_hip = landmarks["right_hip"]
    left_elbow = landmarks["left_elbow"]
    left_wrist = landmarks["left_wrist"]

    output = {}

    # COMMON
    output["shoulder"] = round(dist(left_shoulder, right_shoulder), 1)

    result = {}

    # 🟦 KURTA
    if garment == "kurta":
        result = {
            "shoulder": shoulder,
            "chest": round(shoulder * 1.4, 1),
            "waist": round(hip * 1.2, 1),
            "kurta_length": round(leg_length * 0.55, 1),
            "sleeve_length": dist(landmarks["left_shoulder"], landmarks["left_wrist"])
        }

    # 🟩 PANT
    elif garment == "pant":
        result = {
            "waist": round(hip * 1.1, 1),
            "hip": hip,
            "thigh": round(hip * 0.65, 1),
            "pant_length": leg_length,
            "bottom": round(hip * 0.35, 1)
        }

    # 🟪 LEHENGA
    elif garment == "lehenga":
        result = {
            "waist": round(hip * 1.05, 1),
            "hip": hip,
            "lehenga_length": round(leg_length * 1.05, 1),
            "flare": round(hip * 3.2, 1)
        }
    elif garment == "shirt":
        result = {
            "chest": round(output["shoulder"] * 1.35, 1),
            "waist": round(dist(left_hip, right_hip) * 1.25, 1),
            "sleeve_length": round(dist(left_shoulder, left_wrist), 1),
            "shirt_length": round(dist(left_shoulder, left_hip) * 1.15, 1)
        }

    elif garment == "tshirt":
        result = {
            "chest": round(output["shoulder"] * 1.25, 1),
            "length": round(dist(left_shoulder, left_hip), 1),
            "half_sleeve": round(dist(left_shoulder, left_elbow), 1)
        }

    elif garment == "blouse":
        return blouse_measurements(landmarks, scale, fit)
        #result = {
        #    "bust": round(output["shoulder"] * 1.40, 1),
        #    "under_bust": round(output["shoulder"] * 1.30, 1),
        #    "blouse_length": round(dist(left_shoulder, left_hip) * 0.65, 1),
        #    "sleeve_length": round(dist(left_shoulder, left_elbow), 1)
        #}

    return result
