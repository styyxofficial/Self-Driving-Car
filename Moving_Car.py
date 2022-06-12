import pygame
from pygame.locals import *
from Car import Car
import sys


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


def on_event(event):
    if event.type == QUIT:
        on_cleanup()

    if pygame.key.get_pressed()[K_UP]:
        car_1.move_forward()
        
    if pygame.key.get_pressed()[K_DOWN]:
        car_1.move_backward()
        
    if pygame.key.get_pressed()[K_LEFT]:
        car_1.move_left()
        
    if pygame.key.get_pressed()[K_RIGHT]:
        car_1.move_right()
        

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


while(_running):
    for event in pygame.event.get():
        on_event(event)
    on_loop()
    on_render()
    fpsClock.tick(FPS)


on_cleanup()

# Use this to save genomes
# https://github.com/CodeReclaimers/neat-python/blob/master/neat/checkpoint.py
