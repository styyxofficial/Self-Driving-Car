import numpy as np

class NeuralNetwork:
    def __init__(self):
        # Input Layer: 9
        # Layer 1: 12
        # Layer 2: 9
        # Layer 3: 6
        # Layer 4: 4
        np.random.seed(1)
        
        self.mutation_init_mean = 0
        self.mutation_init_sd = 1
        self.mutation_rate = 0.3
        self.mutation_power = 0.1
        
        
        self.m1 = np.random.normal(self.mutation_init_mean, self.mutation_init_sd, size = (9, 12))
        self.final = np.random.normal(self.mutation_init_mean, self.mutation_init_sd, size = (12, 4))
        
    def calculate(self, input_layer):
        return input_layer @ self.m1 @ self.final
    
    def mutate():
        nums_to_mutate = 