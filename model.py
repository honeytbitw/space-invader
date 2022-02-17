import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Convolution2D, Input, Reshape
from tensorflow.keras.optimizers import Adam

def build_model(height, width, channels, actions):
    model = Sequential()
    model.add(Input(shape=(height,width,channels)))
    model.add(Reshape((height,width,channels,1), input_shape=(height,width,channels)))
    model.add(Convolution2D(32, (8,8), strides=(4,4), activation='relu'))
    model.add(Convolution2D(64, (4,4), strides=(2,2), activation='relu'))
    model.add(Convolution2D(64, (3,3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    model.compile()
    return model