import pyxel
from entity import Entity
from consts.colour import Colour
from typing import List, Tuple
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
        """
        If we can think then move
        :return:
        """
        if super().think():
            self.move()

    def move(self):
        """
        Determine which direction we should move and conditionally set our destination
        :return:
        """
        result = False
    
        if self.movement_type == MovementType.CHASE:
            destination_entity = Entity.all[self.target]
            self.destination = (destination_entity.x, destination_entity.y)
            
        if self.destination is None:
            return result
    
        move_horizontal, destination_offset_boundary_x = self.is_within_destination_and_offset(
            self.x, self.destination[0]
        )
        move_vertical, destination_offset_boundary_y = self.is_within_destination_and_offset(
            self.y, self.destination[1]
        )
    
        if move_horizontal and move_vertical:
            move_horizontal = choice([True, False])
            move_vertical = not move_horizontal
    
        if move_horizontal:
            result = self.move_in_plane(self.x, self.destination[0], destination_offset_boundary_x, self.move_left,
                                        self.move_right)

            return result
        
        elif move_vertical:
            result = self.move_in_plane(self.y, self.destination[1], destination_offset_boundary_y, self.move_up,
                                        self.move_down)
        
            return result
        else:
            
            if self.movement_type == MovementType.PATROL:
                # TODO: Not use a hardcoded range
                self.destination = (randint(0, 200), randint(0, 200))
    
        return False

    def move_in_plane(self,
                      current: int, destination: int,
                      destination_offset_boundary: Tuple[int, int],
                      decrease_position,
                      increase_position):
        """
        For a plane (x-axis or y-axis) should we increase our position or decrease our position
        :param current: current value in the plane
        :param destination: destination value in the plane
        :param destination_offset_boundary: the offset boundaries (min, max)
        :param decrease_position: function to decrease our position in the boundary
        :param increase_position: function to increase our position in the boundary
        :return:
        """
        result = False
        
        if current < destination_offset_boundary[0]:
            increase_position()
            result = True
        elif destination_offset_boundary[0] < current < destination:
            decrease_position()
            result = True
        elif current > destination_offset_boundary[1]:
            decrease_position()
            result = True
        elif destination < current < destination_offset_boundary[1]:
            increase_position()
            result = True
        elif self.target_offset > 0 and current == destination:
            # tie breaking if we're exactly on our target but we need to be at an offset
            if choice([True, False]):
                decrease_position()
            else:
                increase_position()
                
        return result

    def is_within_destination_and_offset(self, current_value, target_value):
        """
        For a plane (x-axis or y-axis) are we within the target and the target +/- the offset
        :param current_value:
        :param target_value:
        :return: bool are we within the boundary, tuple of the boundary
        """
        destination_bounds = (target_value - self.target_offset, target_value + self.target_offset)
        
        if current_value != target_value and (
                (current_value != destination_bounds[0]) or (current_value != destination_bounds[1])):
            return True, destination_bounds
        
        return False, destination_bounds

    def move_left(self):
        """
        Move left on screen
        :return:
        """
        self.x = (self.x - 1) % pyxel.width

    def move_right(self):
        """
        Move right on screen
        :return:
        """
        self.x = (self.x + 1) % pyxel.width

    def move_up(self):
        """
        Move up on screen
        :return:
        """
        self.y = (self.y - 1) % pyxel.width

    def move_down(self):
        """
        Move down on screen
        :return:
        """
        self.y = (self.y + 1) % pyxel.width

