from tracemalloc import start
import numpy as np
import cv2 as cv
from PIL import ImageGrab
from main import start_game
from threading import Thread
from window_capture import WindowCapture
import random
from model import build_model
import tensorflow as tf
import keras
model = keras.models.load_model('model')
print(model.summary())
def displayScreenshot() :
    while True:
        screenshot= WindowCapture('Space Invader').take_screenshot()
        cv.imshow('Computer Vision',screenshot)
        
        if cv.waitKey(1) == ord('q') :
            cv.destroyAllWindows()
            break
        screenshot.shape= (1,562, 784, 3)
        res = model(screenshot)
        action = res.numpy()[0][0]
        print(action)
        if(action>0.5) : 
            print("Right")
        else :
            print("Left")
        

Thread(target = start_game).start()
Thread(target = displayScreenshot).start()