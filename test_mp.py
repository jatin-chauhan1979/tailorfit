import mediapipe as mp


print("Loaded from:", mp.__file__)
print("Version:", getattr(mp, "__version__", "No version"))
print("Has solutions:", hasattr(mp, "solutions"))

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

print("MediaPipe working")
print("MediaPipe version:", mp.__version__)
print("Has solutions:", hasattr(mp, "solutions"))

