import cv2
import os
import numpy as np
from PIL import Image
from aps.settings import BASE_DIR
import face_recognition as fr

from facedetection.models import Usuario


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

class FaceRecognition:
    all_entries = Usuario.objects.all()
    print(all_entries)