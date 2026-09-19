import numpy as np

def calculate(lm, scale):
    def d(p1, p2):
        return round(np.linalg.norm(p1 - p2) * scale, 1)

    shoulder = d(lm["left_shoulder"], lm["right_shoulder"])
    hip = d(lm["left_hip"], lm["right_hip"])
    sleeve = d(lm["left_shoulder"], lm["left_elbow"])

    return {
        "Length": round(d(lm["left_shoulder"], lm["left_hip"]) * 0.55, 1),
        "UpperChest": round(shoulder * 1.25, 1),
        "SleevesLength": sleeve,
        "SleevesRound": round(shoulder * 0.42, 1),
        "NeckFront": round(shoulder * 0.28, 1),
        "NeckBack": round(shoulder * 0.20, 1),
        "TucksLength": round(d(lm["left_shoulder"], lm["left_hip"]) * 0.30, 1),
        "ArmHole": round(shoulder * 0.52, 1),
        "Chest": round(shoulder * 1.40, 1),
        "Waist": round(hip * 1.15, 1),
        "Shoulders": shoulder
    }
