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
        MovableEntity.width_aspect_ratio = pyxel.width

        pyxel.mouse(True)

        self.grid = Grid(App.width, App.height, App.tile_size)
        
        Entity.grid = self.grid

        self.load_level()
        
        self.debug_message = ""
        self.game_message = ""
        
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.npcs = []
        self.items = []
        self.walls = []
        self.score = 0
        self.game_message = ""

    def load_level(self):
        self.reset_game()

        with open('level.txt') as f:
            wall_lines = f.readlines()        
        
        for row_index, row_value in enumerate(wall_lines):            
            for col_index, col_value in enumerate(row_value):
                if col_value == "#":
                    self.add_wall(row_index, col_index)
                elif col_value == "@":
                    self.add_player(row_index, col_index)
                elif col_value == "&":
                    self.add_rabbit(row_index, col_index)
                elif col_value == ".":
                    self.add_speed_down(row_index, col_index)
                elif col_value == "*":
                    self.add_speed_up(row_index, col_index)
                elif col_value == "~":
                    self.add_carrot(row_index, col_index)
                elif col_value == "X":
                    self.add_end(row_index, col_index)

        self.start_rabbit()

    def add_player(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        print("player:", x, y)
        self.player = MovableEntity(x, y, App.tile_size-2, App.tile_size-2, Colour.GREEN, 5)

    def add_rabbit(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        print("rabbit:", x, y)
        self.rabbit = MovableEntity(x, y, App.tile_size-2, App.tile_size-2, Colour.WHITE, 5, False, self.npcs)

    def remove_item(self, item):
        self.grid - item.id
        if item in self.items:
            self.items.remove(item)

    def add_speed_down(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        item = Entity(x, y, App.tile_size-2, App.tile_size-2, Colour.RED, 5, False, self.items)
        item.on_collide = self.apply_speed_down

    def apply_speed_down(self, apply_from, apply_to):
        apply_to.tick_rate += 1
        self.remove_item(apply_from)

    def add_speed_up(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        item = Entity(x, y, App.tile_size-2, App.tile_size-2, Colour.LIGHT_BLUE, 5, False, self.items)
        item.on_collide = self.apply_speed_up

    def apply_speed_up(self, apply_from, apply_to):
        apply_to.tick_rate -= 1
        self.remove_item(apply_from)

    def add_carrot(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        item = Entity(x, y, App.tile_size-2, App.tile_size-2, Colour.ORANGE, 5, False, self.items)
        item.on_collide = self.eat_carrot

    def eat_carrot(self, carrot, eater):
        if eater.id != self.rabbit.id:
            return
        self.remove_item(carrot)
        self.score += 1

    def add_end(self, row, column):
        x, y = self.grid.get_pixel_center(row, column)
        item = Entity(x, y, App.tile_size, App.tile_size, Colour.GREY, 5, False, self.items)
        item.on_collide = self.check_end

    def check_end(self, goal, other):
        if other.id != self.rabbit.id:
            return
        self.game_message = "YOU WIN! Press R to restart"

    def start_rabbit(self):
        self.rabbit.target_offset = App.tile_size * 2
        self.rabbit.target = self.player.id
        self.rabbit.movement_type = MovementType.CHASE

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

    def get_grid_data(self, x, y):
        return self.grid[x, y]


    def update(self):
        if pyxel.btnp(pyxel.constants.KEY_LEFT, self.player.tick_rate, self.player.tick_rate):
            self.player.move_left()
        elif pyxel.btnp(pyxel.constants.KEY_RIGHT, self.player.tick_rate, self.player.tick_rate):
            self.player.move_right()
        elif pyxel.btnp(pyxel.constants.KEY_UP, self.player.tick_rate, self.player.tick_rate):
            self.player.move_up()
        elif pyxel.btnp(pyxel.constants.KEY_DOWN, self.player.tick_rate, self.player.tick_rate):
            self.player.move_down()
        # debug stuffs
        elif pyxel.btnr(pyxel.constants.KEY_PERIOD):
            self.player.tick_rate -= 1
        elif pyxel.btnr(pyxel.constants.KEY_COMMA):
            self.player.tick_rate += 1
        elif pyxel.btnr(pyxel.constants.KEY_R):
            self.load_level()
        elif pyxel.btnr(pyxel.constants.KEY_LEFT_BUTTON):
            self.debug_x_y(pyxel.mouse_x, pyxel.mouse_y)
        # rabbit cheat
        elif pyxel.btnp(pyxel.constants.KEY_W, self.player.tick_rate, self.player.tick_rate):
            self.rabbit.movement_type = MovementType.NONE
            self.rabbit.target = None
            self.rabbit.move_up()
        elif pyxel.btnp(pyxel.constants.KEY_A, self.player.tick_rate, self.player.tick_rate):
            self.rabbit.movement_type = MovementType.NONE
            self.rabbit.target = None
            self.rabbit.move_left()
        elif pyxel.btnp(pyxel.constants.KEY_D, self.player.tick_rate, self.player.tick_rate):
            self.rabbit.movement_type = MovementType.NONE
            self.rabbit.target = None
            self.rabbit.move_right()
        elif pyxel.btnp(pyxel.constants.KEY_S, self.player.tick_rate, self.player.tick_rate):
            self.rabbit.movement_type = MovementType.NONE
            self.rabbit.target = None
            self.rabbit.move_down()
        elif pyxel.btnp(pyxel.constants.KEY_X, self.player.tick_rate, self.player.tick_rate):
            self.start_rabbit()

    def debug_x_y(self, x, y):
        print(self.get_grid_data(x, y))
        print(self.grid.query(
            x, y, k = 8, distance_upper_bound = App.tile_size * 2
        ))

    def draw(self):
        pyxel.cls(0)

        draw_item_ids = False
        items = self.items.copy()
        for item in items:
            item.think()
            item.draw()
            if draw_item_ids:
                pyxel.text(
                    item.top_left[0], 
                    item.top_left[1], 
                    str(item.id), 
                    Colour.BLACK.value
                    )
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
            "score: {a} - herder speed: {b} - rabbit speed: {c}".format(
                a = self.score,
                b = self.player.tick_rate,
                c = self.rabbit.tick_rate
            ), 
            Colour.PINK.value
        )

        if self.game_message != "":
            pyxel.text(
                40, App.height/2,
                self.game_message,
                Colour.LIGHT_GREEN.value
            )

        self.player.draw()

        draw_grid = False
        if draw_grid:
            for point in self.grid.flat_pixel_positions:
                pyxel.pix(point[1], point[0], Colour.PINK.value)

App()