import pyxel
from moveable_entity import MovableEntity
from consts.colour import Colour
from random import choice, randint
from moveable_entity import MovementType

class App:
    
    width = 240
    height = 136
    
    def __init__(self):
        pyxel.init(App.width, App.height, caption = "PyxelTest", fps = 60, scale = 4)

        self.coins = []
        
        #for i in range(0, randint(10, 15)):
        for i in range(0, 1):
            coin = MovableEntity(randint(7, 200), randint(7, 130), 7, 7, Colour.YELLOW, 5, False, self.coins)
            coin.destination = (240/2, 136/2)

        self.player = MovableEntity(10, 10, 7, 7, Colour.GREEN, 5)
        
        # make the last coin chase the player
        coin.target_offset = 14
        coin.target = self.player.id
        coin.movement_type = MovementType.CHASE
        coin.base_colour = Colour.ORANGE.value

        pyxel.run(self.update, self.draw)

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
        
        for coin in self.coins:
            coin.think()
            coin.draw()

App()