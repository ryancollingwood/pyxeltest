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
    tile_size = 8
    
    def __init__(self):
        pyxel.init(App.width, App.height, caption = "PyxelTest", fps = 60, scale = 4)

        self.grid = Grid(App.width, App.height, App.tile_size)
        
        Entity.grid = self.grid
        
        self.npcs = []
        self.items = []
        self.walls = []
        
        wall_text = """
##############################
##############################
#                            #
#            .  &            #
#                    *       #
#                    @       #
#          #####             #
#   ##  ####   #             #
#   #   #      #             #
#   # ### ###  ###  ######## #
#   # #     #    ## #      # #
#   # # ### ###     #  ### # #
#   # #       #######    # # #
#   # # ###############  # # #
#   # #                  # # #
#   # #################### # #
#   #                      # #
##############################
        """.strip()

        wall_lines = wall_text.split('\n')
        for row_index, row_value in enumerate(wall_lines):            
            for col_index, col_value in enumerate(row_value):
                if col_value == "#":
                    self.add_wall(row_index, col_index)
                elif col_value == "@":
                    self.add_player(row_index, col_index)
                elif col_value == "&":
                    self.add_sheep(row_index, col_index)
                elif col_value == ".":
                    self.add_speed_down(row_index, col_index)
                elif col_value == "*":
                    self.add_speed_up(row_index, col_index)

        self.start_sheep()

        self.debug_message = ""
        
        pyxel.run(self.update, self.draw)

    def add_player(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        print("player:", x, y)
        self.player = MovableEntity(x, y, App.tile_size-2, App.tile_size-2, Colour.GREEN, 5)

    def add_sheep(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        print("sheep:", x, y)
        self.sheep = MovableEntity(x, y, App.tile_size-2, App.tile_size-2, Colour.WHITE, 5, False, self.npcs)

    def add_speed_down(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        item = Entity(x, y, App.tile_size-2, App.tile_size-2, Colour.RED, 5, False, self.items)
        item.on_collide = self.apply_speed_down

    def add_speed_up(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        item = Entity(x, y, App.tile_size-2, App.tile_size-2, Colour.LIGHT_BLUE, 5, False, self.items)
        item.on_collide = self.apply_speed_up

    def apply_speed_up(self, apply_from, apply_to):
        apply_to.tick_rate -= 1
        self.grid - apply_from.id
        self.items.remove(apply_from)

    def apply_speed_down(self, apply_from, apply_to):
        apply_to.tick_rate += 1
        self.grid - apply_from.id
        self.items.remove(apply_from)

    def start_sheep(self):
        self.sheep.target_offset = App.tile_size * 2
        self.sheep.target = self.player.id
        self.sheep.movement_type = MovementType.CHASE

    def add_wall(self, row, column):
        # add_at_grid_position
        x, y = self.grid.get_pixel_center(row, column)
        Entity(
            x,
            y,
            App.tile_size, App.tile_size, Colour.BROWN,
            5, True,
            self.walls
        )


    def update(self):
        if pyxel.btnp(pyxel.constants.KEY_LEFT, self.player.tick_rate, self.player.tick_rate):
            self.player.move_left()
        elif pyxel.btnp(pyxel.constants.KEY_RIGHT, self.player.tick_rate, self.player.tick_rate):
            self.player.move_right()
        elif pyxel.btnp(pyxel.constants.KEY_UP, self.player.tick_rate, self.player.tick_rate):
            self.player.move_up()
        elif pyxel.btnp(pyxel.constants.KEY_DOWN, self.player.tick_rate, self.player.tick_rate):
            self.player.move_down()
        elif pyxel.btnr(pyxel.constants.KEY_PERIOD):
            self.player.tick_rate -= 1
        elif pyxel.btnr(pyxel.constants.KEY_COMMA):
            self.player.tick_rate += 1


    def draw(self):
        pyxel.cls(0)

        items = self.items.copy()
        for item in items:
            item.think()
            item.draw()
        del items

        npcs = self.npcs.copy()
        for npc in npcs:
            npc.think()
            npc.draw()
        del npcs
            
        draw_wall_ids = False

        for wall in self.walls:
            wall.draw()
            if draw_wall_ids:
                pyxel.text(
                    wall.top_left[0], 
                    wall.top_left[1], 
                    str(wall.id), 
                    Colour.BLACK.value
                    )

        pyxel.text(
            40, 10, 
            "herder speed: {a} - sheep speed: {b}".format(
                a = self.player.tick_rate,
                b = self.sheep.tick_rate
            ), 
            Colour.PINK.value
        )

        self.player.draw()

        draw_grid = False
        if draw_grid:
            for point in self.grid.flat_pixel_positions:
                pyxel.pix(point[1], point[0], Colour.PINK.value)

App()