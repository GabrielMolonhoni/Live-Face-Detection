# ---- Imports -----

import os
import threading
import cv2
from threading import Thread, Lock
import time
import numpy as np

# ---- Code ----


class FaceDetector(Thread):
    def __init__(self):
        super(FaceDetector, self).__init__()
        print("[INFO] Starting FaceDetector")

        self.running = True
        self.locker = Lock()

        self.ReadFiles()

        print("[INFO] FaceDetector Started")

    def run(self):
        faces = None
        number_of_faces = None

        while self.running:
            with self.locker:
                frame = getattr(self, 'frame', None)
            if frame is not None:
                faces = self.DetectFaces(frame)
                displayer = getattr(self, 'displayer', None)
                if displayer is not None:
                    displayer.UpdateFaces(faces)
            time.sleep(0.001)

    def ReadFiles(self):
        modelPath = os.path.join(os.path.abspath(os.getcwd()),'models', 'res10_300x300_ssd_iter_140000.caffemodel')

        print(modelPath)

        prototxtPath = os.path.join(os.path.abspath(os.getcwd()), 'models', 'deploy.prototxt.txt')

        if not os.path.exists(modelPath):
            raise Exception("Model File does not exist")

        if not os.path.isfile(prototxtPath):
            raise Exception("Config File does not exist")

        print("[INFO] Load Caffe Model")
        self.net = cv2.dnn.readNetFromCaffe(prototxtPath, modelPath)
        print("[INFO] Caffe Model loaded")

    def Stop(self):
        self.running = False

    def DetectFaces(self, frame):
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))

        self.net.setInput(blob)
        faces = self.net.forward()

        detected_faces = []

        for i in range(faces.shape[2]):
            confidence=faces[0, 0, i, 2]
            if confidence > 0.5:
                face = faces[0,0,i,3:7]
                detected_faces.append(face.copy())
            else:
                break
        return np.array(detected_faces).tolist()
        

    def SetDisplayer(self, displayer):
        with self.locker:
            self.displayer=displayer

    def SetFrame(self, frame):
        with self.locker:
            self.frame=frame
