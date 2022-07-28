from calendar import c
from re import X
from tkinter import N
from cv2 import split
import pygame
from pygame.locals import *
from Car import Car
import sys
import neat
import time
import multiprocessing

# def m1():
#     car = Car(car_image, 881, 800, 0)
#     car.draw(screen)

# def m2():
#     global c
#     c = 43
    
# def m3():
#     print(c)

# if __name__== "__main__":
#     # Load Config
#     pygame.init()
#     screen_width = 1920
#     screen_height = 1080
#     screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    
#     background_image = pygame.image.load("images/map.png").convert_alpha()
#     # screen.fill("white")
#     screen.blit(background_image, (0, 0))
    
#     car_image = pygame.image.load("images/car.png").convert_alpha()
#     car_image = pygame.transform.scale(car_image, (100, 50))
    
#     m2()
#     m3()
#     while False:
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.display.quit()
#                 pygame.quit()
#                 sys.exit()
#         m1()
#         pygame.display.flip()

j = [1, 2, 3, 4, 5, 6, 7]
split_lists = [j[x:x+3] for x in range(0, len(j), 3)]
print(split_lists)