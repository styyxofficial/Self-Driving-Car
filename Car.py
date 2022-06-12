from numpy import imag
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
        # self.check_max_acceleration()

        self.linear_velocity += time_unit * self.linear_acceleration
        self.rotational_velocity += time_unit * self.rotational_acceleration

        self.check_max_velocity()

        # print(self.linear_acceleration)
        self.angle += self.rotational_velocity * time_unit
        self.distance_traveled += self.linear_velocity * time_unit

        # Direction times distance to travel
        self.x += math.cos((self.angle) * (math.pi/180)) * (self.linear_velocity * time_unit)
        self.y -= math.sin((self.angle) * (math.pi/180)) * (self.linear_velocity * time_unit)

        self.check_bounds(screen)
        self.collision_detection(screen)
        self.sensors(screen)

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

    def sensors(self, screen):
        """
        Creates multiple visual sensors for the car and measures their distance

        Args:
            screen (Surface): the screen on which the images are displayed
        Returns:
            numpy array of distance values from the sensor
        """

        sensor_offset = [0, 5, 37, 90, -5, -37, -45, -90]
        # angle of sensor 1 is theta=0

        for theta_o in sensor_offset:
            slope = -math.tan((self.angle+theta_o) * (math.pi/180))

            image_center = self.image.get_rect(topleft=(self.x, self.y)).center

            sensor_start = (round(image_center[0] + math.cos((self.angle+theta_o) * (math.pi/180)) * self.image.get_size()[0]/2),
                            round(image_center[1] - math.sin((self.angle+theta_o) * (math.pi/180)) * self.image.get_size()[0]/2))

            #pygame.draw.circle(surface=screen, color="blue", center=sensor_start, radius=4)
            if (sensor_start[0] < image_center[0]):
                flip = -1
            else:
                flip = 1

            # Compute max distance the car has to see
            if (image_center[0]/2 > screen.get_size()[0]/2):
                max_dist = image_center[0]
            else:
                max_dist = screen.get_size()[0] - image_center[0]

            # use point slope for to calculate the new location
            for x1 in range(sensor_start[0], sensor_start[0]+max_dist*flip, flip):
                y1 = -slope * (sensor_start[0]-x1)+sensor_start[1]

                pos = (round(x1), round(y1))

                try:
                    #pygame.draw.circle(surface=screen, color="orange", center=pos, radius=4)
                    if (tuple(screen.get_at(pos)) == (255, 255, 255, 255)):
                        #pygame.draw.line(screen, color="blue", start_pos=sensor_start, end_pos=pos, width=3)
                        pygame.draw.circle(surface=screen, color="blue", center=pos, radius=4)
                        break
                except:
                    # Means the slope was infinite, and the point could not be calculated
                    continue
