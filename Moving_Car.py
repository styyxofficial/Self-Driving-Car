from tkinter import *
import time
from Car import Car


# if in 1 second the car has not changed its position that much, kill the car
window = Tk()

WIDTH = 700
HEIGHT = 700

canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()

car_1 = Car(canvas, 350, 350, 50, 70, 0, 0, "red")


while True:
    car_1.move(3)
    window.update()
    time.sleep(0.032)

window.mainloop()
