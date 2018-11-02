import pyxel
from moveable_entity import MovableEntity
from consts.colour import Colour
from random import choice, randint
from moveable_entity import MovementType
from grid import Grid
from entity import Entity
import game_state

class App:
    
    width = 240
    height = 144
    
    def __init__(self):
        pyxel.init(App.width, App.height, caption = "PyxelTest", fps = 60, scale = 4)

        self.grid = Grid(App.width, App.height, 8)
        
        Entity.grid = self.grid
        
        self.ghosts = []
        self.walls = []
        
        self.spawn_walls()
        ghost = self.spawn_ghosts()

        self.player = MovableEntity(10, 10, 8, 8, Colour.GREEN, 5)

        self.debug_message = ""

        self.make_a_chasing_ghost(ghost)

        pyxel.run(self.update, self.draw)

    def make_a_chasing_ghost(self, ghost):
        ghost.target_offset = 14
        ghost.target = self.player.id
        # make the last ghost chase the player
        ghost.movement_type = MovementType.CHASE
        ghost.base_colour = Colour.ORANGE.value

    def spawn_ghosts(self):
        for i in range(0, randint(10, 15)):
            ghost = MovableEntity(
                randint(8, App.width),
                randint(8, App.height),
                8, 8, Colour.YELLOW,
                5, False,
                self.ghosts
            )
            # converge on the middle to begin with
            ghost.destination = (App.width / 2, App.height / 2)
        return ghost

    def spawn_walls(self):
        for i in range(0, randint(10, 15)):
            x, y = self.grid.get_pos_for_pixels(
                randint(8, App.width),
                randint(8, App.height)
            )
            Entity(
                x,
                y,
                8, 8, Colour.BROWN,
                5, True,
                self.walls
            )

    def update(self):
        if pyxel.btnp(pyxel.constants.KEY_LEFT, 5, 5):
            self.player.move_left()
        elif pyxel.btnp(pyxel.constants.KEY_RIGHT, 5, 5):
            self.player.move_right()
        elif pyxel.btnp(pyxel.constants.KEY_UP, 5, 5):
            self.player.move_up()
        elif pyxel.btnp(pyxel.constants.KEY_DOWN, 5, 5):
            self.player.move_down()

    def draw(self):
        pyxel.cls(0)
        
        self.player.draw()
        
        for coin in self.ghosts:
            coin.think()
            coin.draw()
            
        for wall in self.walls:
            wall.draw()

        pyxel.text(40, 10, str(self.player.movement_direction) + " - " + game_state.debug_message, Colour.PINK.value)

        #for point in self.grid.flat_pixel_positions:
        #    pyxel.pix(point[1], point[0], Colour.PINK.value)


App()