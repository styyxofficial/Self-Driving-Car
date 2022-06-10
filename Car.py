import pygame
from pygame.locals import *
import math
class Car:
    def __init__(self, image, x, y, angle):
        self.image = image
        self.x = x
        self.y = y
        self.angle = angle
    
    def draw(self, screen):
        img = pygame.transform.rotate(self.image, self.angle)
        screen.blit(img, (self.x, self.y))
        
    
    def move_forward(self):
        self.x += math.cos((self.angle+90) * (math.pi/180))
        self.y -= math.sin((self.angle+90) * (math.pi/180))
    
    def move_backward(self):
        self.x -= math.cos((self.angle+90) * (math.pi/180))
        self.y += math.sin((self.angle+90) * (math.pi/180))
    
    def move_left(self):
        self.angle += 1
        
    
    def move_right(self):
        self.angle -= 1