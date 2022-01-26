from random import randint

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Jump")
        pyxel.load("assets/jump_game.pyxres")
        self.score = 0
        self.player_x = 72
        self.player_y = -16
        self.player_dy = 0
        self.is_alive = True
        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        self.floor = [(i * 60, randint(8, 104), True) for i in range(4)]
        self.fruit = [(i * 60, randint(0, 104), randint(0, 2), True)
                      for i in range(4)]
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()
        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor(*v)
        for i, v in enumerate(self.fruit):
            self.fruit[i] = self.update_fruit(*v)

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
        self.player_y += self.player_dy
        self.player_dy = min(self.player_dy + 1, 8)

        if self.player_y > pyxel.height:
            if self.is_alive:
                self.is_alive = False
                pyxel.play(3, 5)
            if self.player_y > 600:
                self.score = 0
                self.player_x = 72
                self.player_y = -16
                self.player_dy = 0
                self.is_alive = True

    def update_floor(self, x, y, is_alive):
        if is_alive:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_dy > 0
            ):
                is_alive = False
                self.score += 10
                self.player_dy = -12
                pyxel.play(3, 3)
        else:
            y += 6
        x -= 4
        if x < -40:
            x += 240
            y = randint(8, 104)
            is_alive = True
        return x, y, is_alive
