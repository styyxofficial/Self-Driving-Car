import pygame
from pygame.locals import *
from Car import Car
import sys


def on_init():
    pygame.init()


on_init()


_running = True
screen = pygame.display.set_mode(
    (500, 500), pygame.HWSURFACE | pygame.DOUBLEBUF)
screen.fill("WHITE")

# Number of ms in 1 time unit
# Needed for acceleration
time_unit = 16
pygame.key.set_repeat(time_unit)

# Load game assests
# Car image used from : https://github.com/NeuralNine/ai-car-simulation/blob/master/car.png
car_image = pygame.image.load("images/car.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (100, 50))
car_1 = Car(car_image, 250, 250, 0)


def on_event(event):
    if event.type == QUIT:
        on_cleanup()

    if pygame.key.get_pressed()[K_DOWN]:
        screen.fill("WHITE")
        car_1.move_backward(time_unit)

    if pygame.key.get_pressed()[K_UP]:
        screen.fill("WHITE")
        car_1.move_forward(time_unit)

    if pygame.key.get_pressed()[K_LEFT]:
        screen.fill("WHITE")
        car_1.move_left()

    if pygame.key.get_pressed()[K_RIGHT]:
        screen.fill("WHITE")
        car_1.move_right()

    # pygame.time.delay(16)


def on_loop():
    pass


def on_render():
    screen.fill("WHITE")
    car_1.friction(time_unit)
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
on_cleanup()
