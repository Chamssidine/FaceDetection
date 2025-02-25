from dataBaseManager import DataBaseManager
from faceDetector  import FaceDetector
import json
import numpy  as np
from userData import UserData
import matplotlib.pyplot as plt


database = DataBaseManager("database")
database.delete_table("table1")
face_detector = FaceDetector()
(success, userData) = face_detector.detect_faces_in("images")

database.create_database("database")
database.create_table("table1")
def json_converter(obj):
    if isinstance(obj, np.ndarray):  
        return obj.tolist()  # Convert numpy array to list
    elif hasattr(obj, "__dict__"):  
        return obj.__dict__  # Convert object attributes to dictionary
    else:
        raise TypeError(f"Type {type(obj)} not serializable")

if(success):
    userData = json.dumps(userData, default=json_converter)
    database.insert(userData, "table1", "database")
    (success,data)  = database.get("table1")

(success,data)  = database.get("table1")

if(success):
    data = json.loads(data)
    for face in data["faces"]:
        plt.imshow(face)
        plt.show()
    
else:
    print("could not load user data")

#

