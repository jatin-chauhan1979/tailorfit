import cv2
import mediapipe as mp
import numpy as np
import math
import os

class GarmentMeasurerImage:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            min_detection_confidence=0.5
        )
    
        self.shirt_sizes = {
            "XS": (70, 84), 
            "S":  (85, 93), 
            "M":  (94, 102),
            "L":  (103, 110), 
            "XL": (111, 120), 
            "XXL": (121, 135)
        }
        self.pant_sizes = {
            "XS": (24, 27), "S": (28, 31), "M": (32, 34),
            "L": (35, 37), "XL": (38, 42)
        }

    @staticmethod
    def dist(p1, p2):
        return math.dist(p1, p2)

    def get_shirt_size(self, chest_cm):
        for size, (lo, hi) in self.shirt_sizes.items():
            if lo <= chest_cm <= hi: return size
        return "S" if chest_cm < 85 else "M"

    def get_pant_size(self, waist_inch):
        for size, (lo, hi) in self.pant_sizes.items():
            if lo <= waist_inch <= hi: return size
        return "S" if waist_inch < 32 else "M"

    def analyze_image(self, image_path, user_height_cm):
        if not os.path.exists(image_path): return None, None
        frame = cv2.imread(image_path)
        if frame is None: return None, None

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = self.pose.process(rgb)
        if not res.pose_landmarks: return frame, None
        lm = res.pose_landmarks.landmark
        
        def xy(i): return int(lm[i].x * w), int(lm[i].y * h)

    
        nose = xy(0)
        l_sh, r_sh = xy(11), xy(12) 
        l_elb, r_elb = xy(13), xy(14)
        l_wri, r_wri = xy(15), xy(16)
        l_hip, r_hip = xy(23), xy(24)
        l_knee, r_knee = xy(25), xy(26)
        l_ank, r_ank = xy(27), xy(28)
        l_heel, r_heel = xy(29), xy(30)

        is_child = user_height_cm < 145
        
        if is_child:
            ratio_nose_to_ankle = 0.85 
            shoulder_multiplier = 1.18 
            chest_multiplier = 2.05 
            waist_ratio = 0.95 
            thigh_ratio = 3.8 
            sleeve_multiplier = 1.10   
        else:
            ratio_nose_to_ankle = 0.88
            shoulder_multiplier = 1.10 
        
            chest_multiplier = 2.10  
            waist_ratio = 0.90       
            thigh_ratio = 4.1        
            sleeve_multiplier = 1.05

        y_nose = nose[1]
        y_ank_avg = (l_ank[1] + r_ank[1]) // 2
        pixel_height = abs(y_ank_avg - y_nose)
        
        if pixel_height == 0: return frame, None
        pixels_per_cm = pixel_height / (user_height_cm * ratio_nose_to_ankle)

    
        skeletal_shoulder_px = self.dist(l_sh, r_sh)
        shoulder_cm = (skeletal_shoulder_px / pixels_per_cm) * shoulder_multiplier
        chest_cm = shoulder_cm * chest_multiplier

        mid_sh = ((l_sh[0]+r_sh[0])//2, (l_sh[1]+r_sh[1])//2)
        mid_hip = ((l_hip[0]+r_hip[0])//2, (l_hip[1]+r_hip[1])//2)
        torso_px = self.dist(mid_sh, mid_hip)
        
        hem_cm = 8 if is_child else 6
        shirt_len_cm = (torso_px / pixels_per_cm) + hem_cm

        waist_y = int(mid_hip[1] - (torso_px * 0.18)) 
        y_heel_avg = (l_heel[1] + r_heel[1]) // 2
        pant_len_cm = abs(y_heel_avg - waist_y) / pixels_per_cm
        
        waist_circ_cm = chest_cm * waist_ratio
        waist_inch = waist_circ_cm / 2.54

    
        hip_width_px = self.dist(l_hip, r_hip)
        thigh_width_cm = (hip_width_px / 2.1) / pixels_per_cm 
        thigh_circ_cm = thigh_width_cm * thigh_ratio

        return frame, {
            "shoulder": shoulder_cm, "chest": chest_cm, "shirt_len": shirt_len_cm,
            "pant_len": pant_len_cm, "waist_cm": waist_circ_cm, 
            "waist_in": waist_inch, "thigh_cm": thigh_circ_cm
        }

if __name__ == "__main__":
    try:
        height = float(input("Enter user height in cm: "))
        front_path = input("FRONT image: ").strip('"').strip("'")
        back_path = input("BACK image:  ").strip('"').strip("'")

        app = GarmentMeasurerImage()
        img_f, d_f = app.analyze_image(front_path, height)
        img_b, d_b = app.analyze_image(back_path, height)

        if d_f and d_b:
            res = {k: (d_f[k] + d_b[k]) / 2 for k in d_f if isinstance(d_f[k], (int, float))}
            shirt_size = app.get_shirt_size(res['chest'])
            pant_size_label = app.get_pant_size(res['waist_in'])

            print(f"\nHeight: {int(height)} cm\nGarment Measurements (Approx)\n")
            print("Shirt:")
            print(f"- Length: ~{int(res['shirt_len']-1)}–{int(res['shirt_len'])+1} cm")
            print(f"- Chest: ~{int(res['chest']-1)}–{int(res['chest'])+1} cm")
            print(f"- Shoulder: ~{int(res['shoulder']-1)}–{int(res['shoulder'])+1} cm")
            print(f"- Size: {shirt_size}\n")
            
            print("Pant:")
            print(f"- Length: ~{int(res['pant_len']-1)}–{int(res['pant_len'])+1} cm")
            print(f"- Waist: ~{int(res['waist_cm']-1)}–{int(res['waist_cm'])+1} cm")
            print(f"- Thigh: ~{int(res['thigh_cm']-1)}–{int(res['thigh_cm'])+1} cm")
            print(f"- Size: {pant_size_label} ({int(res['waist_in'])}-{int(res['waist_in'])+1})\n")
            
            cv2.imshow("Result", img_f)
            cv2.waitKey(0)
    except Exception as e:
        print(f"Error: {e}")