import numpy as np

def blouse_measurements(lm, scale, fit):
    def d(p1, p2):
        return round(np.linalg.norm(p1 - p2) * scale, 1)

    # Core landmarks
    ls = lm["left_shoulder"]
    rs = lm["right_shoulder"]
    le = lm["left_elbow"]
    lw = lm["left_wrist"]
    lh = lm["left_hip"]
    rh = lm["right_hip"]

    shoulder = d(ls, rs)
    hip_width = d(lh, rh)
    sleeve_length = d(ls, le)

    # Base measurements (Regular fit base)
    base = {
        "Length": round(d(ls, lh) * 0.55, 1),
        "Upper Chest": round(shoulder * 1.25, 1),
        "Sleeves Length": sleeve_length,
        "Sleeves Round": round(shoulder * 0.42, 1),
        "Neck Front": round(shoulder * 0.28, 1),
        "Neck Back": round(shoulder * 0.20, 1),
        "Tucks Length": round(d(ls, lh) * 0.30, 1),
        "Arm Hole": round(shoulder * 0.52, 1),
        "Chest": round(shoulder * 1.40, 1),
        "Waist": round(hip_width * 1.15, 1),
        "Shoulders": shoulder
    }

    return apply_blouse_fit(base, fit)

def apply_blouse_fit(measurements, fit):
    rules = BLOUSE_FIT_ALLOWANCE.get(fit, BLOUSE_FIT_ALLOWANCE["regular"])
    final = {}

    for k, v in measurements.items():
        final[k] = round(v + rules.get(k, 0), 1)

    final["Fit Type"] = fit
    return final

BLOUSE_FIT_ALLOWANCE = {
    "slim": {
        "Chest": 0,
        "Waist": 0,
        "Upper Chest": 0
    },
    "regular": {
        "Chest": 2,
        "Waist": 2,
        "Upper Chest": 1
    },
    "loose": {
        "Chest": 4,
        "Waist": 4,
        "Upper Chest": 2
    }
}
