# ---- Imports -----

import os
import cv2
from threading import Thread,Lock

# ---- Code ----

class Camera():
    def __init__(self):
        print("[INFO] Initializing Camera")

        self.running = False
        self.image = None

        self.lockerCameraThread = Lock()
        self.lockerGetImage = Lock()

        self.OpenCamera()
        print("[INFO] Camera Opened")

    def OpenCamera(self):
        try:
            self.camera = cv2.VideoCapture(0)
            self.running = True
        except:
            print("[ERROR] Failed to open camera")
            self.camera.release()
           # os._exit(1)

    def Start(self):
        self.cameraThread = Thread(target= self.Run, args=())
        self.cameraThread.start()
        return self

    def Run(self):
        print("[INFO] Camera running")
        while self.running:
            try:
                self.lockerCameraThread.acquire()

                ret, frame = self.camera.read()
                self.image = frame.copy()

                self.lockerCameraThread.release()
            except:
                print("[ERROR] Error getting frame from camera")
                raise Exception("Error getting frame from camera")

        self.camera.release()
        print("[INFO] Camera Stopped")

    def Stop(self):
        self.running = False
        self.cameraThread.join()

    def GetImage(self):
        self.lockerGetImage.acquire()
        frame = self.image.copy()
        self.lockerGetImage.release()
        return frame
