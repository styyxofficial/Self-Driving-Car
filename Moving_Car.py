import pygame
from pygame.locals import *
from Car import Car
import sys

def on_init():
    pygame.init()

on_init()


    
_running = True
screen = pygame.display.set_mode((500,500), pygame.HWSURFACE | pygame.DOUBLEBUF)
screen.fill("WHITE")
pygame.key.set_repeat(16)

# Load game assests
car_image = pygame.image.load("images/rectangle.png").convert()
car_1 = Car(car_image, 250, 250)



def on_event(event):
    if event.type == QUIT:
        on_cleanup()
        
        
    if pygame.key.get_pressed()[K_DOWN]:
        screen.fill("WHITE")
        car_1.move_down()
        
    if pygame.key.get_pressed()[K_UP]:
        screen.fill("WHITE")
        car_1.move_up()
    
    if pygame.key.get_pressed()[K_LEFT]:
        screen.fill("WHITE")
        car_1.move_left()
    
    if pygame.key.get_pressed()[K_RIGHT]:
        screen.fill("WHITE")
        car_1.move_right()

def on_loop():
    pass
    
def on_render():
    pygame.display.flip()
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