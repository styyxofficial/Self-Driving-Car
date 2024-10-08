from turtle import back
import pygame
from pygame.locals import *
from Car import Car
import sys
import neat
import time
import multiprocessing
import visualize
import configparser

screen_width = None
screen_height = None

_running = None

FPS = None
fpsClock = None

# Load game assests
# map as background image

# Car image used from : https://github.com/NeuralNine/ai-car-simulation/blob/master/car.png


screen = None

car_image = None
car_image = None
background_image = None



def on_init():
    pygame.init()


def on_event(event):
    if event.type == QUIT:
        on_cleanup()

    # Implement the following if you want to manually control the car
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
    _running = False
    pygame.display.quit()
    pygame.quit()
    sys.exit()
    exit(1)

"""
This version of an eval_function is not standard. Typically the eval_function accepts 1 genome and returns its fitness. Here we use multiple genomes in a list because we want each CPU Core to handle many cars at the same time.
In order for this to work, the parallel.py file in NEAT has to be modified to support evaluating genomes as lists, and over multiple CPU cores with different memory allocations.
"""
def eval_genome2(genomes, config, initial_dict):
    try:
        global screen_width, screen_height, _running, FPS, fpsClock, screen, car_image, background_image
        
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
        background_image = pygame.image.load(initial_dict["map_path"]).convert_alpha()


        # Empty Collections For Nets and Cars
        nets = []
        cars = []
        fitness = []
        
        # For All Genomes Passed Create A New Neural Network
        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0
            fitness.append(0)
            
            cars.append(Car(car_image, int(initial_dict["car_start_x"]), int(initial_dict["car_start_y"]), 0))
        
        # End generation after 15 seconds
        timeout = time.time() + 15  # 15 seconds after current time

        while _running:
            # End the game when the X is pressed
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            
            cars_alive = 0
            screen.blit(background_image, (0, 0))
            
            for i, car in enumerate(cars):
                if car.is_alive:
                    cars_alive += 1
                    fitness[i] = car.get_fitness()
                    
                    output = nets[i].activate(car.get_data())
                    choice = output.index(max(output))
                    if choice == 0:
                        car.move_forward()
                    elif choice == 1:
                        car.move_backward()
                    elif choice == 2:
                        car.move_left()
                    else:
                        car.move_right()

                    car.update(screen)
                    car.draw(screen)
            
            pygame.display.flip()

            if cars_alive == 0:
                break
            if time.time() > timeout:
                break
            
            fpsClock.tick(FPS)
            
        return fitness
    except:
        return


if __name__ == '__main__':
    on_init()
    
    # Initialize your experiment with # of generations and how many CPU cores you want to run on, the map, and starting location of the car
    initial_settings = configparser.RawConfigParser()
    initial_settings.read('initialization.txt')
    initial_dict = dict(initial_settings.items('INITIALIZATION'))
    generations = int(initial_dict['generations'])
    cpu_cores = int(initial_dict['cpu_cores'])

    config_path = "neat_config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)
    
    # Create Population And Add Reporters
    population = neat.Population(config, initial_dict)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    pe = neat.ParallelEvaluator(cpu_cores, eval_genome2, maxtasksperchild=generations)

    winner = population.run(pe.evaluate, generations)
    
    # Draw the neural network
    # Only draw the network if the best genome/winner was returned. If the program is cancelled before completing the first iteration, then there will be no winner assigned.
    if winner:
        node_names = {0: 'Forward', 1: 'Backward', 2: 'Left', 3:'Right'}
        visualize.draw_net(config, winner, True, node_names=node_names)
        visualize.plot_stats(stats, ylog=False, view=True)
        visualize.plot_species(stats, view=True)

    on_cleanup()

    # Use this to save genomes
    # https://github.com/CodeReclaimers/neat-python/blob/master/neat/checkpoint.py

    # Use this to visualize the network
    # https://ai.stackexchange.com/questions/13948/library-for-rendering-neural-network-neat

    # Use for parallelization
    # https://github.com/CodeReclaimers/neat-python/blob/master/examples/xor/evolve-feedforward-parallel.py

