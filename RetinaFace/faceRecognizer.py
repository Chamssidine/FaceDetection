from deepface import DeepFace

import os

img1_path = "D:/DEVS/Memoire version finale/FaceDetection/RetinaFace/images/zuck.jpg"
img2_path = "D:/DEVS/Memoire version finale/FaceDetection/RetinaFace/images/zuckerberg.jpg"

# Check if files exist
if not os.path.exists(img1_path):
    print(f"Error: {img1_path} does not exist.")
if not os.path.exists(img2_path):
    print(f"Error: {img2_path} does not exist.")

# Now call DeepFace
obj = DeepFace.verify(img1_path, img2_path, model_name="ArcFace", detector_backend="retinaface")
print(obj)
