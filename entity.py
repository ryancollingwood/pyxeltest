import pyxel
from consts.colour import Colour
from typing import List

class Entity:
    
    id = 0
    all = {}
    grid = None
    
    def __init__(self,
                 x: int, y: int, height: int, width: int,
                 base_colour: Colour, tick_rate: int = 5,
                 is_solid: bool = True, parent_collection: List = None
                 ):
        
        Entity.id += 1
        self.id = Entity.id
        
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.base_colour = base_colour.value
        self.last_tick = pyxel.frame_count
        self.tick_rate = tick_rate
        self.is_solid = is_solid

        self.top_left = None
        self.top_right = None
        self.middle_left = None
        self.middle = None
        self.middle_right = None
        self.bottom_left = None
        self.bottom_right = None
        self.top_middle = None
        self.bottom_middle = None
        
        self.refresh_dimensions()
        
        if parent_collection is not None:
            parent_collection.append(self)
            
        Entity.all[self.id] = self
    
    def refresh_dimensions(self):
        half_height = self.height / 2
        half_width = self.width / 2
        
        self.top_left = (self.x - half_width, self.y - half_height)
        self.top_middle = (self.x, self.y - half_height)
        self.top_right = (self.x + half_width, self.y - half_height)
        self.bottom_left = (self.x - half_width, self.y + half_height)
        self.bottom_middle = (self.x, self.y + half_height)
        self.bottom_right = (self.x + half_width, self.y + half_height)
        self.middle_right = (self.x + half_width, self.y)
        self.middle_left = (self.x - half_width, self.y)
        self.middle = (self.x, self.y)
        
        Entity.grid[self.middle] = self.id

    def can_think(self):
        if pyxel.frame_count - self.last_tick > self.tick_rate:
            return True

        return False

    def think(self):
        if self.can_think():
            self.last_tick = pyxel.frame_count
        else:
            return False
        
        return True
        
    def draw(self):
        pyxel.rect(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            self.base_colour
            )


