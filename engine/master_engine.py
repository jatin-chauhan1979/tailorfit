import numpy as np
from engine.landmark_detector import detect_landmarks
from engine.fit_adjustment import apply_fit
from engine.fit_recommendation import recommend_fit

from garments import blouse, shirt, tshirt, kurta, pant, lehenga

GARMENT_MAP = {
    "blouse": blouse,
    "shirt": shirt,
    "tshirt": tshirt,
    "kurta": kurta,
    "pant": pant,
    "lehenga": lehenga
}

def calculate_body_scale(lm, height_cm):
    body_px = np.linalg.norm(
        lm["nose"] - (lm["left_ankle"] + lm["right_ankle"]) / 2
    )
    return height_cm / body_px

def measure(image_path, height_cm, garment, fit=None):
    lm = detect_landmarks(image_path)
    if not lm:
        return {"error": "Body not detected"}

    scale = calculate_body_scale(lm, height_cm)

    garment_module = GARMENT_MAP.get(garment)
    if not garment_module:
        return {"error": "Invalid garment"}

    base = garment_module.calculate(lm, scale)

    if not fit:
        fit = recommend_fit(base)

    final = apply_fit(base, fit)

    return {
        "Garment": garment,
        "RecommendedFit": fit,
        "Measurements": final,
        "HeightCM": height_cm
    }
