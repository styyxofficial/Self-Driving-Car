import math


class Car:

    def __init__(self, canvas, x, y, len, wid, xVelocity, yVelocity, color):
        """
        @param x: center x position of the rectangle
        @param y: center y position of the rectangle
        @param len: length of the rectangle
        @param wid: width of the rectangle
        """

        self.canvas = canvas

        x_0 = x - len/2
        y_0 = y - wid/2
        x_1 = x + len/2
        y_1 = y + wid/2

        self.image = canvas.create_rectangle(x_0, y_0, x_1, y_1, fill=color)
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity

    def move(self, time):
        # function of time
        velocity = math.sin(time)

        self.canvas.move(self.image, self.xVelocity, self.yVelocity)
