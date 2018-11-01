import pyxel
from entity import Entity
from consts.colour import Colour
from typing import List
from random import choice, randint
from enum import Enum


class MovementType(Enum):
    PATROL = 1
    CHASE = 2


class MovableEntity(Entity):
    
    def __init__(self,
                 x: int, y: int, height: int, width: int,
                 base_colour: Colour, tick_rate: int = 5,
                 is_solid: bool = True, parent_collection: List = None,
                 movement_type: MovementType = MovementType.PATROL,
                 target = None, target_offset = 0
                 ):
        
        super().__init__(x, y, height, width, base_colour, tick_rate, is_solid, parent_collection)
        self.destination = None
        self.movement_type = movement_type
        self.target = target
        self.target_offset = target_offset
        
    def think(self):
        if super().think():
            self.move()

    def move(self):
        result = False
    
        if self.movement_type == MovementType.CHASE:
            destination = Entity.all[self.target]
            self.destination = (destination.x, destination.y)
            
        if self.destination is None:
            return result
    
        move_horizontal = False
        move_vertical = False
    
        if self.x != self.destination[0]:
            move_horizontal = True
        if self.y != self.destination[1]:
            move_vertical = True
    
        if move_horizontal and move_vertical:
            move_horizontal = choice([True, False])
            move_vertical = not move_horizontal
    
        if move_horizontal:
            if self.destination[0] - self.x > self.target_offset:
                self.move_right()
                result = True
            elif self.x - self.destination[0] > self.target_offset:
                self.move_left()
                result = True
            elif self.destination[0] > self.x - self.target_offset:
                self.move_left()
                result = True
            elif self.x < self.destination[0] + self.target_offset:
                self.move_right()
                result = True

            return result
        
        elif move_vertical:
            if self.y + self.target_offset < self.destination[1]:
                self.move_down()
                result = True
            elif self.y - self.target_offset > self.destination[1]:
                self.move_up()
                result = True
        
            return result
        else:
            
            if self.movement_type == MovementType.PATROL:
                self.destination = (randint(0, 200), randint(0, 200))
    
        return False

    def move_left(self):
        self.x = (self.x - 1) % pyxel.width

    def move_right(self):
        self.x = (self.x + 1) % pyxel.width

    def move_up(self):
        self.y = (self.y - 1) % pyxel.width

    def move_down(self):
        self.y = (self.y + 1) % pyxel.width

