from re import L
import numpy as np
import pygame
from pygame.locals import *
import math
import threading


# With this current implementation of car, you cannot choose the accerlation. You apply a set acceleration for a certain amount of time
# Future work should include being able to change the accleration, however that cannot be implemented using the NEAT algorithm as far as I know
class Car:
    def __init__(self, image, x, y, angle):
        self.image = image
        self.x = x
        self.y = y
        self.angle = angle
        self.distance_traveled = 0.0
        self.is_alive = True
        
        
        # position from 3 seconds ago, to check if the car has moved a lot
        self.old_x = 0
        self.old_y = 0
        
        # angle of the sensors
        self.sensor_offset = [0, 5, 37, 90, -5, -37, -90]
        
        # distance of each sensor
        self.distances = np.zeros(len(self.sensor_offset))

        # Acceleration
        self.linear_acceleration = 0.0
        self.rotational_acceleration = 0.0

        # Affected by time and acceleration
        self.linear_velocity = 0.0
        self.rotational_velocity = 0.0
        
        # Average velocity calculation used for fitness
        self.total_linear_velocity = 0
        self.ticks = 1
        
        self.check_position()

    def update(self, screen):

        time_unit = 1.0

        self.friction()

        self.linear_velocity += time_unit * self.linear_acceleration
        self.rotational_velocity += time_unit * self.rotational_acceleration

        self.check_max_velocity()
        
        self.total_linear_velocity += self.linear_velocity
        self.ticks += 1
        
        self.angle += self.rotational_velocity * time_unit
        self.distance_traveled += self.linear_velocity * time_unit

        # Direction times distance to travel
        self.x += math.cos((self.angle) * (math.pi/180)) * (self.linear_velocity * time_unit)
        self.y -= math.sin((self.angle) * (math.pi/180)) * (self.linear_velocity * time_unit)

        self.check_bounds(screen)
        self.collision_detection(screen)
        self.sensors(screen)

        self.linear_acceleration = 0
        self.rotational_acceleration = 0
        
    def draw(self, screen):
        img = pygame.transform.rotate(self.image, self.angle)
        screen.blit(img, img.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center))

    def move_forward(self):
        """
        Apply a linear force forward
        """
        self.linear_acceleration = 0.5

    def move_backward(self):
        """
        Apply a linear force backward
        """
        self.linear_acceleration = -0.5

    def move_left(self):
        """
        Apply a rotational force counter clockwise
        """
        self.rotational_acceleration = 0.5

    def move_right(self):
        """
        Apply a rotational force clockwise
        """
        self.rotational_acceleration = -0.5

    def friction(self):
        """
        Create a frictional force that will stop the car when there is no acceleration
        """
        if (self.linear_velocity > 0):
            self.linear_acceleration -= 0.25
        elif (self.linear_velocity < 0):
            self.linear_acceleration += 0.25

        if (self.rotational_velocity > 0):
            self.rotational_acceleration -= 0.25
        elif (self.rotational_velocity < 0):
            self.rotational_acceleration += 0.25

    def check_max_velocity(self):
        """
        Limit the velocity of the car
        """
        if (self.linear_velocity > 20):
            self.linear_velocity = 20
        if (self.linear_velocity < -20):
            self.linear_velocity = -20
        if (self.rotational_velocity > 9):
            self.rotational_velocity = 9
        if (self.rotational_velocity < -9):
            self.rotational_velocity = -9

    def check_bounds(self, screen):
        """
        Check if the car is off the screen, and if it is, move it back onto the screen
        """
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
        Detect if the car has hit the walls of the track
        
         *___________* 4
         |           |
         |           |
         |           |
        *|___________|* 1

        Collisions are checked on the corners of the car, marked by asterisks, moving clockwise
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
                self.is_alive = False

    def sensors(self, screen):
        """
        Creates multiple visual sensors for the car and measures their distance

        Args:
            screen (Surface): the screen on which the images are displayed
        Returns:
            numpy array of distance values from the sensor
        """

        # i represents the index of the sensor
        for i, theta_o in enumerate(self.sensor_offset):
            slope = -math.tan((self.angle+theta_o) * (math.pi/180))

            image_center = self.image.get_rect(topleft=(self.x, self.y)).center

            # Angle of the corner of the car
            corner_angle = abs(math.degrees(math.atan((self.image.get_size()[1]/2) / (self.image.get_size()[0]/2))) )
            
            if abs(theta_o)<corner_angle:
                h = abs((self.image.get_size()[0]/2) / (math.cos(math.radians(theta_o))))
                sensor_start = (round(image_center[0] + h*math.cos(math.radians(theta_o+self.angle))),
                                round(image_center[1] - h*math.sin(math.radians(theta_o+self.angle))))
            else:
                h = abs((self.image.get_size()[1]/2) / (math.sin(math.radians(theta_o))))
                sensor_start = (round(image_center[0] + h*math.cos(math.radians(theta_o+self.angle))),
                                round(image_center[1] - h*math.sin(math.radians(theta_o+self.angle))))
            
            # Flip the sensor measurement if the car is facing left
            if (sensor_start[0] < image_center[0]):
                flip = -1
            else:
                flip = 1

            # Compute max distance the car has to see
            if (image_center[0]/2 > screen.get_size()[0]/2):
                max_dist = image_center[0]
            else:
                max_dist = screen.get_size()[0] - image_center[0]

            # use point slope form to calculate the new location
            for x1 in range(sensor_start[0], sensor_start[0]+max_dist*flip, flip):
                y1 = -slope * (sensor_start[0]-x1)+sensor_start[1]

                pos = (round(x1), round(y1))
                
                try:
                    if (tuple(screen.get_at(pos)) == (255, 255, 255, 255)):
                        self.distances[i] = math.sqrt((pos[0]-image_center[0])**2 + (pos[1]-image_center[1])**2)
                        break
                except:
                    # Means the slope was infinite, and the point could not be calculated
                    continue
        return self.distances
    
    def is_alive(self):
        """
        Returns:
            is_alive: boolean to see if the car is still alive.
        """
        return self.is_alive
    
    def get_data(self):
        """
        Returns:
            numpy array: Array of sensor values and velocity data
        """
        return np.append(self.distances, [self.linear_velocity, self.rotational_velocity])
    
    def check_position(self):
        """
        Checks if the position of the car has changed significantly in the last 1 seconds
        """
        th = threading.Timer(2.0, self.check_position)
        th.daemon  = True
        th.start()
        
        d = math.sqrt((self.x-self.old_x)**2 + (self.y-self.old_y)**2)
        
        if (d < 50):
            self.is_alive = False
        
        self.old_x = self.x
        self.old_y = self.y

    def get_fitness(self):
        """
        We want to maximize the forward speed and distance of the car
        
        Returns:
            float: Fitness. Dependent on the distance and average velocity of the car.
        """
        # Calculate fitness based on average velocity
        return ((self.distance_traveled/100) * (((self.total_linear_velocity/self.ticks)**2)/100))
