import numpy as np

class NeuralNetwork:
    def __init__(self, input, hidden, output):
        self.input = input
        self.hidden = hidden
        self.output = output
        self.create_neural_network()

    def create_neural_network(self):
        # Xavier initialization for weights
        self.W1 = np.random.randn(self.input, self.hidden) * np.sqrt(2. / self.input)
        self.b1 = np.zeros((self.hidden,))
        self.W2 = np.random.randn(self.hidden, self.output) * np.sqrt(2. / self.hidden)
        self.b2 = np.zeros((self.output,))

    def relu(self, x):
        return np.maximum(0, x)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def predict(self, X):
        X = np.array([X])  # Ensure batch dimension
        z1 = np.dot(X, self.W1) + self.b1
        a1 = self.relu(z1)
        z2 = np.dot(a1, self.W2) + self.b2
        output = self.sigmoid(z2)
        return output

    def get_weights(self):
        return [self.W1.copy(), self.b1.copy(), self.W2.copy(), self.b2.copy()]

    def set_weights(self, weights):
        self.W1 = weights[0].copy()
        self.b1 = weights[1].copy()
        self.W2 = weights[2].copy()
        self.b2 = weights[3].copy()

