import pyxel

from game import Game
from entity import Entity
from consts.colour import Colour


class App:
    
    width = 240
    height = 144
    tile_size = 8
    
    def __init__(self):
        pyxel.init(App.width, App.height, caption = "Rabbit Herder", fps = 60, scale = 4)
        pyxel.mouse(True)

        self.game = Game(App.width, App.height, App.tile_size, pyxel.width)
        
        pyxel.run(self.update, self.draw)

    def update(self):
        player = self.game.player
        rabbit = self.game.rabbit

        if pyxel.btnp(pyxel.constants.KEY_LEFT, player.tick_rate, player.tick_rate):
            player.move_left()
        elif pyxel.btnp(pyxel.constants.KEY_RIGHT, player.tick_rate, player.tick_rate):
            player.move_right()
        elif pyxel.btnp(pyxel.constants.KEY_UP, player.tick_rate, player.tick_rate):
            player.move_up()
        elif pyxel.btnp(pyxel.constants.KEY_DOWN, player.tick_rate, player.tick_rate):
            player.move_down()
        # debug stuffs
        elif pyxel.btnr(pyxel.constants.KEY_PERIOD):
            player.tick_rate -= 1
        elif pyxel.btnr(pyxel.constants.KEY_COMMA):
            player.tick_rate += 1
        elif pyxel.btnr(pyxel.constants.KEY_R):
            self.game.load_level()
        elif pyxel.btnr(pyxel.constants.KEY_LEFT_BUTTON):
            self.game.debug_x_y(pyxel.mouse_x, pyxel.mouse_y)
        # rabbit cheat
        elif pyxel.btnp(pyxel.constants.KEY_W, player.tick_rate, player.tick_rate):
            rabbit.movement_type = MovementType.NONE
            rabbit.target = None
            rabbit.move_up()
        elif pyxel.btnp(pyxel.constants.KEY_A, player.tick_rate, player.tick_rate):
            rabbit.movement_type = MovementType.NONE
            rabbit.target = None
            rabbit.move_left()
        elif pyxel.btnp(pyxel.constants.KEY_D, player.tick_rate, player.tick_rate):
            rabbit.movement_type = MovementType.NONE
            rabbit.target = None
            rabbit.move_right()
        elif pyxel.btnp(pyxel.constants.KEY_S, player.tick_rate, player.tick_rate):
            rabbit.movement_type = MovementType.NONE
            rabbit.target = None
            rabbit.move_down()
        elif pyxel.btnp(pyxel.constants.KEY_X, player.tick_rate, player.tick_rate):
            self.game.start_rabbit()

    def draw_entity(self, entity: Entity):
        pyxel.rect(
            entity.x - entity.half_width, entity.y - entity.half_height,
            entity.x + entity.half_width, entity.y + entity.half_height,
            entity.base_colour
            )        

    def draw(self):

        pyxel.cls(0)
        game = self.game
        walls = self.game.walls

        draw_item_ids = False
        items = game.items.copy()
        for item in items:
            item.think(pyxel.frame_count)
            self.draw_entity(item)

            if draw_item_ids:
                pyxel.text(
                    item.top_left[0], 
                    item.top_left[1], 
                    str(item.id), 
                    Colour.BLACK.value
                    )
        del items

        npcs = game.npcs.copy()
        for npc in npcs:
            npc.think(pyxel.frame_count)
            self.draw_entity(npc)

        del npcs
            
        draw_wall_ids = False

        for wall in walls:
            self.draw_entity(wall)

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
                a = game.score,
                b = game.player.tick_rate,
                c = game.rabbit.tick_rate
            ), 
            Colour.PINK.value
        )

        if game.game_message != "":
            pyxel.text(
                40, App.height/2,
                self.game_message,
                Colour.LIGHT_GREEN.value
            )

        self.draw_entity(game.player)

        draw_grid = False
        if draw_grid:
            grid = self.game.grid
            for point in grid.flat_pixel_positions:
                pyxel.pix(point[1], point[0], Colour.PINK.value)

App()