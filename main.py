import pyxel
from entity import Entity

class App:
    def __init__(self):
        pyxel.init(240, 136, caption = "PyxelTest", fps = 60, scale = 3)
        self.x = 0

        self.player = Entity(10, 10, 7, 7, 9, 5)
        self.coin = Entity(20, 10, 7, 7, 11, 5)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.constants.KEY_LEFT, 5, 5):
            self.player.move_left()
        elif pyxel.btnp(pyxel.constants.KEY_RIGHT, 5, 5):
            self.player.move_right()
            
    def draw(self):
        pyxel.cls(0)
        self.player.draw()
        self.coin.draw()

App()