from turtle import back
import pygame
from pygame.locals import *
from Car import Car
import sys
import neat
import time
import multiprocessing
import visualize


# Load Config
# screen_width = 1920
# screen_height = 1080

# _running = True

# FPS = 60
# fpsClock = pygame.time.Clock()

# # Load game assests
# # map as background image

# # Car image used from : https://github.com/NeuralNine/ai-car-simulation/blob/master/car.png


# screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)

# car_image = pygame.image.load("images/car.png").convert_alpha()
# car_image = pygame.transform.scale(car_image, (100, 50))
# background_image = pygame.image.load("images/map.png").convert_alpha()

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


def run_simulation(genomes, config):
    # Empty Collections For Nets and Cars
    nets = []
    cars = []

    
    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car(car_image, 881, 800, 0))

    # timeout = time.time() + 60*5   # 5 minutes from now
    # timeout = time.time() + 15   # 10 seconds from now

    timeout = time.time() + 15  # 15 seconds after current time

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

            if car.is_alive:
                cars_alive += 1
                genomes[i][1].fitness = car.get_fitness()

                output = nets[i].activate(car.get_data())
                # This needs to be tested
                choice = output.index(max(output))
                if choice == 0:
                    car.move_forward()
                elif choice == 1:
                    car.move_backward()
                elif choice == 2:
                    car.move_left()
                else:
                    car.move_right()

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

def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    car = Car(car_image, 881, 800, 0)

    timeout = time.time() + 15  # 15 seconds after current time
        
    while car.is_alive:
        # End the game when the X is pressed
        for event in pygame.event.get():
            on_event(event)
            
        screen.blit(background_image, (0, 0))
        
        

        output = net.activate(car.get_data())
        # This needs to be tested
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
        
        genome.fitness = car.get_fitness()
        pygame.display.flip()
        
        #fpsClock.tick(FPS)
    return car.get_fitness()

def eval_genome2(genomes, config):
    
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
    background_image = pygame.image.load("images/map.png").convert_alpha()


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
        
        cars.append(Car(car_image, 881, 800, 0))
        
    timeout = time.time() + 15  # 15 seconds after current time
    #print(genomes)
    #print(_running)
    while _running:
        cars_alive = 0
        screen.blit(background_image, (0, 0))
        
        for i, car in enumerate(cars):
            if car.is_alive:
                cars_alive += 1
                genomes[i][1].fitness = car.get_fitness()
                fitness[i] = car.get_fitness()
                
                output = nets[i].activate(car.get_data())
                # This needs to be tested
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
        #print(cars_alive)
        if cars_alive == 0:
            break
        if time.time() > timeout:
            break
        
        fpsClock.tick(FPS)
    #print(fitness)
    return fitness


if __name__ == '__main__':
    on_init()
    
    config_path = "config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)
    
    config_path2 = "config2.txt"
    config2 = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path2)
    
    config_path3 = "config3.txt"
    config3 = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path3)

    config_path4 = "config4.txt"
    config4 = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path4)
    
    config_list = [config, config2, config3]
    
    # Create Population And Add Reporters
    population = neat.Population(config_list)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run for up to 400 generations.
    pe = neat.ParallelEvaluator(6, eval_genome2, maxtaskperchild=36*2)
    winner = population.run(pe.evaluate, 200)
    
    # Draw the net
    node_names = {0: 'Forward', 1: 'Backward', 2: 'Left', 3:'Right'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    
    
    # Run Simulation For A Maximum of 1000 Generations
    #population.run(run_simulation, 10000)



    on_cleanup()

    # Use this to save genomes
    # https://github.com/CodeReclaimers/neat-python/blob/master/neat/checkpoint.py


    # Use this to visualize the network
    # https://ai.stackexchange.com/questions/13948/library-for-rendering-neural-network-neat

    # Use for parallelization
    # https://github.com/CodeReclaimers/neat-python/blob/master/examples/xor/evolve-feedforward-parallel.py

