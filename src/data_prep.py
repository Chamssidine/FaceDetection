from genericpath import exists
from posixpath import basename, dirname
from typing import Any, Text
from imutils import paths
import numpy as np
import cv2
import os
from PIL import Image


faces_cascades = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_alt.xml')
def checkDir(dir_name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    for dir in BASE_DIR:
        if os.path.exists(dir_name):
            return False
        else:
            os.makedirs(dir_name,7777)
            return dir_name

def checkContenus(dir_name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    os.path.join(BASE_DIR,dir_name)
    for(root, dirs, files) in os.walk(dir_name):
        for file in files :
            path = os.path.join(root)
            print(path)
            if str(path) != 0:
                if file != 0:
                     return True
                else:
                    return False
            else:
                return True
def detect_face(image):
    faces = faces_cascades.detectMultiScale(image,1.1,7,minSize= (30,30) )
    if faces is not None:
        for (x,y,h,w)in faces:
            roi_img = image[y:y+h,x:x+w]
            return roi_img
#fonction de redimensionnement  
def rescale(img,scale=0.4):
    return cv2.resize(img,(int(img.shape[1]*scale),int(img.shape[0]*scale)),interpolation=cv2.INTER_AREA)

def nombre_image(source_dir):
    count = 0
    for image_path in paths.list_images(source_dir):
        count+=1
    return count

#fonction de normalisation
def normalizer(image):
    img_gray = Image.fromarray(image,'L')
    image = np.array(img_gray,'uint8')
    #image = cv2.resize(image,(200,200),interpolation=cv2.cv2.INTER_AREA)
    image = cv2.equalizeHist(image)
    normalized = np.zeros((300,300))
    image = cv2.normalize(image,normalized,0, 255, cv2.NORM_MINMAX)
    return image


#recupérer les images et détéctés les visages qui y présentent
def fetch_all_images(source_dir):
    print("[INFO:Préparation des données]")
    print("[INFO:#######################]")
    totale = nombre_image(source_dir)
    print("[INFO]nombre totale d'images:",totale)
    print("[INFO:récupération des images]")
    print("[INFO:#######################]")
    print("[INFO]traitement en cours...")
    counter = 0
    i  = 0
    count = 0
    _dir = []
    path = ""
    tets = "="
    for imagePath in paths.list_images(source_dir):
       
        if count==int(totale/2):
            pourcent=(count*100)/totale
            print("[INFO]",int(pourcent),"% terminés")
        if count==int(totale/3):
            pourcent=(count*100)/totale
            print("[INFO]",int(pourcent),"% terminés")
        if count==totale:
            pourcent=(count*100)/totale
            print("[INFO]",int(pourcent),"% terminés")
        if str(imagePath.split(os.path.sep)[-2]) == "test" or str(imagePath.split(os.path.sep)[-2]) == "test_resized":
            continue;
        if str(imagePath.split(os.path.sep)[-2]).find("pf") == 0:
            continue;
        if str(imagePath.split(os.path.sep)[-2]).find("mm") == 0:
            image = cv2.imread(imagePath)  
            totale_row=nombre_image(source_dir+"/"+imagePath.split(os.path.sep)[-2])
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray,(200,200),interpolation=cv2.cv2.INTER_AREA)
            faces = faces_cascades.detectMultiScale(gray,1.2,1, minSize= (30,30))
            if len(faces) is not None:
                for(x, y, h, w) in faces:
                    roi_img = gray[y:y+h,x:x+w]
                    path = "dataset/visages_avec_masque/"
                    checkDir(path)
                    # roi_img = cv2.resize(roi_img,(200,200),interpolation=cv2.cv2.INTER_AREA)
                    cv2.imwrite(path+str(counter)+".jpeg",roi_img)
                counter+=1
            if counter==totale_row: 
                counter = 0
            count+=1
        if str(imagePath.split(os.path.sep)[-2]).find("pp") == 0:
            
            if i == 0:
                _dir.append(imagePath.split(os.path.sep)[-2])
                image = cv2.imread(imagePath)
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                faces = faces_cascades.detectMultiScale(gray,1.0485258,7, minSize= (30,30))
                for(x, y, h, w)in faces:
                    roi_img = gray[y:y+h, x:x+w]
                    roi_img = detect_face(roi_img)
                    # roi_img = cv2.resize(roi_img,(200,200),interpolation=cv2.cv2.INTER_AREA)
                    path = "dataset/"+str(_dir[i]).replace("pp_","")+"/"
                    checkDir(path)

                    cv2.imwrite(path+str(counter)+".jpg",roi_img)
                count+=1
            else:
                
                if _dir[i-1] == imagePath.split(os.path.sep)[-2]:
                    path = "dataset/"+str(_dir[i-1]).replace("pp_","")+"/"
                    _dir.append(imagePath.split(os.path.sep)[-2])
                else:
                    _dir.append(imagePath.split(os.path.sep)[-2])
                    path = "dataset/"+str(_dir[i]).replace("pp_","")+"/"
                    counter = 0
                    checkDir(path)
                image = cv2.imread(imagePath)  
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

                faces = faces_cascades.detectMultiScale(gray,1.0485258,7, minSize= (30,30))
                if len(faces) is not None:
                    for(x, y, h, w) in faces:
                        roi_img = gray[y:y+h,x:x+w]
                        roi_img = detect_face(roi_img)
                        if roi_img is not None:
                            # roi_img = cv2.resize(roi_img,(200,200),interpolation=cv2.cv2.INTER_AREA)
                            cv2.imwrite(path+str(counter)+".jpeg",roi_img)
                        #  else:
                        #      print(path)
                        #     # cv2.imwrite(path+str(counter)+".jpeg",roi_img)
                    counter+=1
                count+=1
            i+=1
if checkContenus("images/") == True:
    print("le dossier n'est pas vide")
    fetch_all_images("images")
    
else:
    print("echec")

print("[INFO]:opération terminée avec succès")
cv2.waitKey(0) 