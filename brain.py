import tensorflow as tf
import numpy as np

class NeuralNetwork:

    def __init__(self, input, hidden, output) :
        self.input = input
        self.hidden = hidden
        self.output = output
        self.create_neural_network()

    def create_neural_network(self):
        self.model = tf.keras.Sequential()

        self.model.add(tf.keras.layers.Dense(self.hidden, activation='relu', input_shape=[self.input]))
        self.model.add(tf.keras.layers.Dense(self.output, activation='sigmoid'))

        # self.model.compile('adam', loss=tf.losses.BinaryCrossentropy, metrics=['accuracy'])
        # self.model.summary()

    def predict(self, X):
        return self.model.predict(np.array([X]))

