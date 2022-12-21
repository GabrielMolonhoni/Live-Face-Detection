
import cv2
import time
import numpy as np
from camera import Camera
from threading import Thread,Lock

class Displayer:
    def __init__(self, camera, faceDetector):
        self.camera = camera
        self.facedetector = faceDetector

        self.facedetector.SetDisplayer(self)

        self.faces = []
        self.number_of_faces = 0

        self.locker = Lock()
        self.lockerGetFace = Lock()

    def Show(self):
        print("[INFO] Graphical Interface Running")
        print("[INFO] PRESS 'ESC' TO CLOSE!")
        while True:
            frame = self.camera.GetImage()
            self.facedetector.SetFrame(frame)

            faces = self.GetFaces()

            if len(faces) > 0:
                frame = self.UpdateFrame(frame, faces)
            time.sleep(0.001)
            if(frame is not None):
                cv2.imshow('video', frame)
            k = cv2.waitKey(27)
            if k == 27:
                self.camera.Stop()
                self.facedetector.Stop()
                break
        cv2.destroyAllWindows()
        print("[INFO] Graphical Interface Stopped")
        

    def UpdateFrame(self, frame, faces):
        h ,w = frame.shape[:2]
        
        if len(faces) > 0 :
            for i in range(len(faces)):
                box = faces[i][:] * np.array([w,h,w,h])
                (x,y,x1,y1) = box.astype("int")
                cv2.rectangle(frame, (x,y), (x1,y1), (0,0,255), 2)   
            return frame                
        else: return frame

        return frame

    def UpdateFaces(self, faces):
        with self.locker:
            self.faces = faces

    def GetFaces(self):
        self.lockerGetFace.acquire()
        faces = self.faces
        self.lockerGetFace.release()
        return faces


