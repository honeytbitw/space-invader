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

model = build_model(562, 784, 3,2)
def action():
    return random.choice([0,1])
def displayScreenshot() :
    while True:
        screenshot = WindowCapture('Space Invader').take_screenshot()
        print(screenshot.shape)
        # data= tf.expand_dims(screenshot, axis =-1)
        # screenshot.shape = (None,562,784,3)
        model(screenshot)
        # action = model(frame) //20fps
        # game(action)
        # frame = np.array(screenshot)
        # screenshot = cv.cvtColor(frame,cv.COLOR_RGB2BGR)
        cv.imshow('Computer Vision',screenshot)
        
        if cv.waitKey(1) == ord('q') :
            cv.destroyAllWindows()
            break

Thread(target = start_game).start()
Thread(target = displayScreenshot).start()