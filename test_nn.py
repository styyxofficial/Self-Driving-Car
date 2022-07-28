from NeuralNetwork import NeuralNetwork
import numpy as np
input_layer = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2])

nn = NeuralNetwork()

print(nn.calculate(input_layer))