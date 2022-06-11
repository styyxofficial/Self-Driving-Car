import pygame
from pygame.locals import *
import math


class Car:
    def __init__(self, image, x, y, angle):
        self.image = image
        self.x = x
        self.y = y
        self.angle = angle
        self.distance_traveled = 0.0

        # Acceleration that is controlled by arrow keys
        self.linear_acceleration = 0.0
        self.rotational_acceleration = 0.0

        # Affected by time and acceleration
        self.linear_velocity = 0.0
        self.rotational_velocity = 0.0

    def draw(self, screen):

        time_unit = 1.0

        self.friction()
        #self.check_max_acceleration()

        self.linear_velocity += time_unit * self.linear_acceleration
        self.rotational_velocity += time_unit * self.rotational_acceleration

        self.check_max_velocity()

        #print(self.linear_acceleration)
        self.angle += self.rotational_velocity * time_unit
        self.distance_traveled += self.linear_velocity * time_unit

        # Direction times distance to travel
        self.x += math.cos((self.angle) * (math.pi/180)) * (self.linear_velocity * time_unit)
        self.y -= math.sin((self.angle) * (math.pi/180)) * (self.linear_velocity * time_unit)

        self.check_bounds()

        img = pygame.transform.rotate(self.image, self.angle)

        # screen.blit(img, (self.x, self.y))
        screen.blit(img, img.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center))
        
        self.linear_acceleration = 0
        self.rotational_acceleration = 0

    def move_forward(self, time_unit):
        time_unit = 1
        self.linear_acceleration = 2

    def move_backward(self, time_unit):
        time_unit = 1
        self.linear_acceleration = -2

    def move_left(self):
        self.rotational_acceleration += 1

    def move_right(self):
        self.rotational_acceleration -= 1

    def friction(self):
        # By multiplying with the velocity, we get an effective terminal velocity
        # Higher number will allow the car to move faster
        terminal_velocity = 2
    
        if (self.linear_velocity > 0):
            self.linear_acceleration -= 1
        elif (self.linear_velocity < 0):
            self.linear_acceleration += 1
        
        
        
        if (self.rotational_velocity > 0):
            self.rotational_acceleration -= 0.5
        elif (self.rotational_velocity < 0):
            self.rotational_acceleration += 0.5


    def check_max_acceleration(self):
        if (self.linear_acceleration > 4):
            self.linear_acceleration = 4
        if (self.linear_acceleration < -4):
            self.linear_acceleration = -4
        if (self.rotational_acceleration > 4):
            self.rotational_acceleration = 4
        if (self.rotational_acceleration < -4):
            self.rotational_acceleration = -4

    def check_max_velocity(self):
        if (self.linear_velocity > 20):
            self.linear_velocity = 20
        if (self.linear_velocity < -20):
            self.linear_velocity = -20
        if (self.rotational_velocity > 9):
            self.rotational_velocity = 9
        if (self.rotational_velocity < -9):
            self.rotational_velocity = -9
        

    def check_bounds(self):
        if (self.x < 0):
            self.x = 1
        if (self.x > 500-self.image.get_size()[0]):
            self.x = 499 - self.image.get_size()[0]
        if (self.y < 0):
            self.y = 0
        if (self.y > 500-self.image.get_size()[1]):
            self.y = 499 - self.image.get_size()[1]
