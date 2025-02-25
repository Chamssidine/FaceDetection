import os
from imutils import paths
import numpy as np
import cv2

def resize(image):
    scale = 650/(image.shape[1]+image.shape[0])
    width = int(image.shape[1]*scale)
    height = int(image.shape[0]*scale-0.01)
    image = cv2.resize(image,(720,800),cv2.INTER_AREA)
    return image


for imagedir in paths.list_images("images/pp_chams/00100sPORTRAIT_00100_BURST20210822112119518_COVER.jpg"):
    image = cv2.imread(imagedir)
    image = resize(image)
    cv2.imwrite("images/pp_andrea/s"+imagedir.split(os.path.sep)[-1],image)
  
