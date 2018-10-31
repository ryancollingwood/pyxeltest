import pyxel

class Entity:
    def __init__(self, x, y, height, width, base_colour, tick_rate):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.base_colour = base_colour
        self.last_tick = pyxel.frame_count
        self.tick_rate = tick_rate

    def move_left(self):
        self.x = (self.x - 1) % pyxel.width
    
    def move_right(self):
        self.x = (self.x + 1) % pyxel.width

    def can_think(self):
        if pyxel.frame_count % self.tick_rate == 0:            
            return True

        return False 

    def think(self):
        if self.can_think:
            self.last_tick = pyxel.frame_count
        else:
            return
        

    def draw(self):
        pyxel.rect(
            self.x, self.y, 
            self.x + self.width, self.y + self.height, 
            self.base_colour
            )

    


