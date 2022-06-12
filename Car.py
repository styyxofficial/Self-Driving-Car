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

        self.check_bounds(screen)
        self.collision_detection(screen)
        
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
        if (self.linear_velocity > 0):
            self.linear_acceleration -= 1
        elif (self.linear_velocity < 0):
            self.linear_acceleration += 1
        
        
        if (self.rotational_velocity > 0):
            self.rotational_acceleration -= 0.5
        elif (self.rotational_velocity < 0):
            self.rotational_acceleration += 0.5

    def check_max_velocity(self):
        if (self.linear_velocity > 20):
            self.linear_velocity = 20
        if (self.linear_velocity < -20):
            self.linear_velocity = -20
        if (self.rotational_velocity > 9):
            self.rotational_velocity = 9
        if (self.rotational_velocity < -9):
            self.rotational_velocity = -9
        

    def check_bounds(self, screen):
        if (self.x < 15):
            self.x = 15
        if (self.x > screen.get_size()[0]-self.image.get_size()[0]-15):
            self.x = screen.get_size()[0] - self.image.get_size()[0]-15
        if (self.y < 40):
            self.y = 40
        if (self.y > screen.get_size()[1] - self.image.get_size()[1] - 40):
            self.y = screen.get_size()[1] - self.image.get_size()[1] - 40
            
    def collision_detection(self, screen):
        
        """
         *___________* 4
         |           |
         |           |
         |           |
        *|___________|* 1
        
        Stars are where the collisions are checked, moving counter clockwise
        """
        
        length_to_corner = math.sqrt((self.image.get_size()[0]/2)**2 + (self.image.get_size()[1]/2)**2)
        angle_to_corner = [(-self.angle) * (math.pi/180) + math.atan((self.image.get_size()[1]/2)/(self.image.get_size()[0]/2)),
                           (-self.angle) * (math.pi/180) + math.pi + math.atan((-self.image.get_size()[1]/2)/(self.image.get_size()[0]/2)),
                           (-self.angle) * (math.pi/180) + math.pi - math.atan((-self.image.get_size()[1]/2)/(self.image.get_size()[0]/2)),
                           (-self.angle) * (math.pi/180) + math.atan((self.image.get_size()[1]/2)/(-self.image.get_size()[0]/2))]
        
        image_center = self.image.get_rect(topleft=(self.x, self.y)).center
        
        for i in range(len(angle_to_corner)):
            corner = (round(length_to_corner * math.cos(angle_to_corner[i]) + image_center[0]), round(length_to_corner * math.sin(angle_to_corner[i]) + image_center[1]))
            
            if (tuple(screen.get_at(corner)) == (255, 255, 255, 255)):
                pygame.draw.circle(surface=screen, color="red", center=corner, radius=4)
            else:
                pygame.draw.circle(surface=screen, color="green", center=corner, radius=4)
                
        
        