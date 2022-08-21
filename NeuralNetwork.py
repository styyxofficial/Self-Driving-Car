import numpy as np
import random
import copy

class NeuralNetwork:
    def __init__(self, layers=None):
        # Input Layer: 9
        # Layer 1: 12
        # Layer 2: 9
        # Layer 3: 6
        # Layer 4: 4
        
        self.mutation_init_mean = 0
        self.mutation_init_sd = 1
        self.mutation_rate = 0.3
        self.mutation_power = 0.5

        if layers == None:
            self.layers = [
                np.random.normal(self.mutation_init_mean, self.mutation_init_sd, size = (9, 6)), # Layer 1
                np.random.normal(self.mutation_init_mean, self.mutation_init_sd, size = (6, 6)), # Layer 2
                #np.random.normal(self.mutation_init_mean, self.mutation_init_sd, size = (9, 5)), # Layer 3
                np.random.normal(self.mutation_init_mean, self.mutation_init_sd, size = (6, 5)) # Output Layer
            ]
        else:
            self.layers = copy.deepcopy(layers)
        
    def relu(self, x):
        return max(0, x)
    
    def calculate(self, input_layer):
        current_calc = input_layer
        
        func = np.vectorize(self.relu)
        
        for layer in self.layers:
            current_calc = current_calc @ layer
            current_calc = func(current_calc)
            
        return current_calc
    
    def mutate(self):
        temp_layers = self.layers
        for layer in temp_layers:
            nums_to_change = layer.size * self.mutation_rate
            
            for _ in range(round(nums_to_change)):
                r = random.randint(0, layer.shape[0]-1)
                c = random.randint(0, layer.shape[1]-1)
                layer[r, c] = layer[r, c] + np.random.normal(0, self.mutation_power, 1)
        return temp_layers
    
    # Working mutation model
    def mutate2(self):
        for layer in self.layers:
            nums_to_change = layer.size * self.mutation_rate
            
            for _ in range(round(nums_to_change)):
                r = random.randint(0, layer.shape[0]-1)
                c = random.randint(0, layer.shape[1]-1)
                layer[r, c] = layer[r, c] + np.random.normal(0, self.mutation_power, 1)
    
    
        """
        Mutate given layers and saves it to current layer
        """
    def mutate3(self, layers):
        layers2 = copy.deepcopy(layers)
        for layer in layers2:
            nums_to_change = layer.size * self.mutation_rate
            
            for _ in range(round(nums_to_change)):
                r = random.randint(0, layer.shape[0]-1)
                c = random.randint(0, layer.shape[1]-1)
                layer[r, c] = layer[r, c] + np.random.normal(0, self.mutation_power, 1)
                
        self.layers = layers2
    
    # similar to mutate 2, but it only mutates 1 thing at a time
    def mutate4(self):
        layer_to_mutate = random.randint(0, len(self.layers)-1)
        r = random.randint(0, self.layers[layer_to_mutate].shape[0]-1)
        c = random.randint(0, self.layers[layer_to_mutate].shape[1]-1)

        self.layers[layer_to_mutate][r, c] = self.layers[layer_to_mutate][r, c] + np.random.normal(0, self.mutation_power, 1)
                        
    def set_layers(self, layers):
        self.layers = layers
    
    def set_mutations(self, mutation_rate, mutation_power):
        self.mutation_rate = mutation_rate
        self.mutation_power = mutation_power
                
            
    