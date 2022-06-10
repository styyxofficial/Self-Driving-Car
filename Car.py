class Car:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    
    def move_up(self):
        self.y -= 1
    
    def move_down(self):
        self.y += 1
    
    def move_left(self):
        self.x -= 1
    
    def move_right(self):
        self.x += 1