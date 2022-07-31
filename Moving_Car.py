from turtle import back
import pygame
from pygame.locals import *
from sklearn import neural_network
from Car import Car
import sys
import neat
import time
import multiprocessing
import visualize
from NeuralNetwork import NeuralNetwork
import copy
import numpy as np


# Load Config
screen_width = 1920
screen_height = 1080

_running = True

FPS = 60
fpsClock = pygame.time.Clock()

# Load game assests
# map as background image

# Car image used from : https://github.com/NeuralNine/ai-car-simulation/blob/master/car.png


screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)

car_image = pygame.image.load("images/car.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (100, 50))
background_image = pygame.image.load("images/map.png").convert_alpha()

# screen_width = None
# screen_height = None

# _running = None

# FPS = None
# fpsClock = None

# Load game assests
# map as background image

# Car image used from : https://github.com/NeuralNine/ai-car-simulation/blob/master/car.png


# screen = None

# car_image = None
# car_image = None
# background_image = None



def on_init():
    pygame.init()


def on_event(event):
    if event.type == QUIT:
        on_cleanup()

    # if pygame.key.get_pressed()[K_UP]:
    #     car_1.move_forward()

    # if pygame.key.get_pressed()[K_DOWN]:
    #     car_1.move_backward()

    # if pygame.key.get_pressed()[K_LEFT]:
    #     car_1.move_left()

    # if pygame.key.get_pressed()[K_RIGHT]:
    #      car_1.move_right()


def on_loop():
    pass


def on_render():
    screen.blit(background_image, (0, 0))
    car_1.get_data()
    car_1.draw(screen)
    pygame.display.flip()


def on_cleanup():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def run_simulation(num_cars, run_iter):
    # Empty Collections For Nets and Cars
    
    
    
    # For All Genomes Passed Create A New Neural Network
    # for i in range(num_cars):
        
    #     #print(nn.layers[0][0])
    #     nets[i] = nn
        
        

    # timeout = time.time() + 60*5   # 5 minutes from now
    # timeout = time.time() + 15   # 10 seconds from now
    best_layer, best_fitness = (None, 0)
    generation = 0

    for _ in range(run_iter):
        
        nets = [None] * num_cars
        cars = [None] * num_cars
    
        for i in range(num_cars):
            nn = NeuralNetwork(layers=best_layer)
            
            if best_fitness>90 | generation>50:
                nn.set_mutations(mutation_rate=0.08, mutation_power=0.0001)
                        
            if best_layer!=None:
                nn.mutate2()
                
            nets[i] = nn
            cars[i] = Car(car_image, 881, 800, 0)
            
        nets[0] = NeuralNetwork(layers=best_layer)
        
        print("Generation:", generation)
        # print("Num cars", len(cars))
        # print(nets[2].layers)
        best_net_idx, best_fitness = method2(nets, cars)
        
        # Randomly initialize cars until they have a good start (minimum fitness to begin mutations)
        if best_fitness > 10:
            best_layer = nets[best_net_idx].layers
        
        
            
        # for i in range(num_cars):
        #     nets[i].mutate3(best_net.layers)
            
        # nets[0] = best_net
        
        #print(len(nets))
        #print(best_net)
        generation += 1
    
    print(best_layer)
    
        

def method2(nets, cars):
    
    timeout = time.time() + 15  # 15 seconds after current time

    #print(nets)
    while(_running):

        # End the game when the X is pressed
        for event in pygame.event.get():
            on_event(event)

        # For Each Car see if its alive
        # Get the action it should take
        # Draw the car

        screen.blit(background_image, (0, 0))

        cars_alive = 0
        for i, car in enumerate(cars):
            # print(car.is_alive, i)
            if car.is_alive:
                cars_alive += 1

                output = nets[i].calculate(car.get_data())
                # This needs to be tested
                choice = output.argmax()
                if choice == 0:
                    car.move_forward()
                elif choice == 1:
                    car.move_backward()
                elif choice == 2:
                    car.move_left()
                elif choice == 3:
                    car.move_right()

                car.update(screen)
                car.draw(screen)
        pygame.display.flip()

        if cars_alive == 0:
            break

        if time.time() > timeout:
            break

        # if time.time()>timeout:
        #    break

        # on_loop()
        # on_render()
        fpsClock.tick(FPS)
    
    max_fitness = -1000000000
    best_net_idx = 0
    for i, car in enumerate(cars):
        if car.get_fitness() > max_fitness:
            max_fitness = car.get_fitness()
            best_net_idx = i
    
    print(max_fitness, best_net_idx)
    
    return best_net_idx, max_fitness


if __name__ == '__main__':
    on_init()
    
    run_simulation(15, 200)


    on_cleanup()

    # Use this to save genomes
    # https://github.com/CodeReclaimers/neat-python/blob/master/neat/checkpoint.py


    # Use this to visualize the network
    # https://ai.stackexchange.com/questions/13948/library-for-rendering-neural-network-neat

    # Use for parallelization
    # https://github.com/CodeReclaimers/neat-python/blob/master/examples/xor/evolve-feedforward-parallel.py

