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
        self.half_height = height / 2
        self.half_width = width / 2
        self.base_colour = base_colour.value
        self.last_tick = pyxel.frame_count
        self.tick_rate = tick_rate
        self.is_solid = is_solid
        self.on_collide = None

        self.top_left = None
        self.top_right = None
        self.middle_left = None
        self.middle = None
        self.middle_right = None
        self.bottom_left = None
        self.bottom_right = None
        self.top_middle = None
        self.bottom_middle = None
        self.grid_pixels = None
        
        self.refresh_dimensions()
        
        if parent_collection is not None:
            parent_collection.append(self)
            
        Entity.all[self.id] = self
    
    def __str__(self):
        return "{id} - {x},{y} - {colour}".format(
            id = self.id,
            x = self.x,
            y = self.y,
            colour = self.base_colour
        )

    def __repr__(self):
        return self.__str__()

    def refresh_dimensions(self):        
        self.top_left = (self.x - self.half_width, self.y - self.half_height)
        self.top_middle = (self.x, self.y - self.half_height)
        self.top_right = (self.x + self.half_width, self.y - self.half_height)
        self.bottom_left = (self.x - self.half_width, self.y + self.half_height)
        self.bottom_middle = (self.x, self.y + self.half_height)
        self.bottom_right = (self.x + self.half_width, self.y + self.half_height)
        self.middle_right = (self.x + self.half_width, self.y)
        self.middle_left = (self.x - self.half_width, self.y)
        self.middle = (self.x, self.y)
        self.grid_pixels = Entity.grid.get_pos_for_pixels(self.x, self.y)

        # again check for collision
        existing_entity_id = Entity.grid[self.middle] 
        if existing_entity_id != self.id:
            self.collide(existing_entity_id)

        Entity.grid[self.middle] = self.id

    def collide(self, other_id):
        if other_id != self.id:
            if other_id in Entity.all: 
                other_entity = Entity.all[other_id]
                if other_entity.on_collide is not None:
                    other_entity.on_collide(other_entity, self)
                if other_entity.is_solid:
                    return [other_entity]
        return []

    def check_collision_point(self, search_x, search_y):
        
        # remove self from grid so we dont
        # find ourselves
        Entity.grid - self.id

        collision_items = Entity.grid.query(
            search_x, search_y, k = 2,
            )
    
        # now add self back to grid
        Entity.grid[self.x, self.x, self.id]
 
        if collision_items is not None:
            print(self.id, collision_items)
            # todo probably a list comprehension here         
            for i, collision_item in enumerate(collision_items):
                
                if collision_item[0]:
                    if collision_item[0] == 0:
                        continue
                    if collision_item[1] > self.width:
                        continue
                    
                    return self.collide(collision_item[0])
        return []

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
            self.x - self.half_width, self.y - self.half_height,
            self.x + self.half_width, self.y + self.half_height,
            self.base_colour
            )


