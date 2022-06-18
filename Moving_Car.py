from tkinter import N
import pygame
from pygame.locals import *
from Car import Car
import sys
import neat

def on_init():  
    pygame.init()


on_init()

screen_width = 1920
screen_height = 1080

_running = True
screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
screen.fill("WHITE")


# Number of ms in 1 time unit
# Needed for acceleration
time_unit = 15
pygame.key.set_repeat(time_unit)

FPS = 60
fpsClock = pygame.time.Clock()

# Load game assests
# map as background image
background_image = pygame.image.load("images/map.png").convert_alpha()
# Car image used from : https://github.com/NeuralNine/ai-car-simulation/blob/master/car.png
car_image = pygame.image.load("images/car.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (100, 50))
car_1 = Car(car_image, 881, 800, 0)
#car_1 = Car(car_image, 500, 500, 0)


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
    #timeout = time.time() + 15   # 10 seconds from now
    
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
                #### This needs to be tested
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
        
        
        if cars_alive==0:
            break
        
        # if time.time()>timeout:
        #    break
        
        #on_loop()
        #on_render()
        fpsClock.tick(FPS)
    

# Load Config
config_path = "config.txt"
config = neat.config.Config(neat.DefaultGenome,
                            neat.DefaultReproduction,
                            neat.DefaultSpeciesSet,
                            neat.DefaultStagnation,
                            config_path)

# Create Population And Add Reporters
population = neat.Population(config)
population.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
population.add_reporter(stats)

# Run Simulation For A Maximum of 1000 Generations
population.run(run_simulation, 1000)
    

on_cleanup()

# Use this to save genomes
# https://github.com/CodeReclaimers/neat-python/blob/master/neat/checkpoint.py


