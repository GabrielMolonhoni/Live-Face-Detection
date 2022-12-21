# ---- Imports -----

from email import message
import cv2
import time
import tensorflow as tf

from camera import Camera
from FaceDetector import FaceDetector
from interface import Displayer

# ---- Code ----

def main():
    try:
        faceDetector = FaceDetector()
        faceDetector.start()

        camera = Camera().Start()
        time.sleep(2)
        
        videoPlayer = Displayer(camera, faceDetector)
        videoPlayer.Show()
        
    except:
        print("[ERROR] Exception ocurred...")
        print("[INFO] Closing")
        exit(1)

if __name__ == "__main__":
    main()