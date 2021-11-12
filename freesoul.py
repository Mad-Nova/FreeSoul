import arcade
import json
import fsfun

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Freesoul Development Version"
SCALING = 1

class FreeSoulGame(arcade.Window):


    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.all_sprites = arcade.SpriteList()

        self.setup()


    def setup(self):
        # Load savegame json file as a python dictionary
        with open('savegame.json') as f:
            savedata = json.load(f)

        self.paused = False
        self.checkpoint = savedata['checkpoint']
        self.timer = savedata['time']
        self.spacetime = fsfun.produceSpaceTime(self.timer)
        self.timedilation = 1

        if self.checkpoint == 0:
            arcade.set_background_color(arcade.color.BLACK)
        else:
            arcade.set_background_color(arcade.color.GRAY)

        self.freesoul = arcade.Sprite("images/freesoul00001.png", SCALING)
        self.freesoul.center_y = self.height / 2
        self.freesoul.left = self.width / 2
        self.all_sprites.append(self.freesoul)


    def on_draw(self):
        arcade.start_render()
        if self.checkpoint == 0:
            arcade.draw_text("Philosophical text here",
            SCREEN_WIDTH/2-240,SCREEN_HEIGHT/2,
            arcade.color.RED,48,160,'left',"Calibri")
        else:
            arcade.draw_text("%4i Y    %1i M    %1i D    %1i H    %2i M    %2i S" 
            %(self.spacetime["yrs"],self.spacetime["mon"],self.spacetime["day"],self.spacetime["hrs"],self.spacetime["min"],self.spacetime["sec"]),
            5,SCREEN_HEIGHT-35,
            arcade.color.BLACK,30,160,'left',"Calibri")
        if self.paused:
            arcade.draw_text("Paused",SCREEN_WIDTH/2-90,SCREEN_HEIGHT-120,arcade.color.BLACK,60,160,'left',"times new roman")
            arcade.draw_text("Press Q to save and quit",SCREEN_WIDTH/2-170,SCREEN_HEIGHT-160,arcade.color.BLACK,30,160,'left',"times new roman")
            arcade.draw_text("Press ESCAPE to continue",SCREEN_WIDTH/2-190,SCREEN_HEIGHT-200,arcade.color.BLACK,30,160,'left',"times new roman")
        self.all_sprites.draw()


    def on_update(self, delta_time: float):
        if self.paused:
            return
        self.timer = self.timer + delta_time
        self.spacetime = fsfun.produceSpaceTime(self.timer)
        self.all_sprites.update()


    def on_key_press(self, symbol, modifiers):
        if (symbol == arcade.key.SPACE) and self.checkpoint == 0:
            self.checkpoint = 1
            arcade.set_background_color(arcade.color.GRAY)

        if (symbol == arcade.key.ESCAPE) and self.checkpoint != 0:
            self.paused = not self.paused

        if symbol == arcade.key.Q and self.paused:
            self.savegame()
            arcade.close_window()

        if symbol == arcade.key.W:
            self.freesoul.change_y = 7

        if symbol == arcade.key.S:
            self.freesoul.change_y = -7

        if symbol == arcade.key.A:
            self.freesoul.change_x = -7

        if symbol == arcade.key.D:
            self.freesoul.change_x = 7


    def on_key_release(self, symbol: int, modifiers: int):
        if (
            symbol == arcade.key.W
            or symbol == arcade.key.S
        ):
            self.freesoul.change_y = 0
        if (
            symbol == arcade.key.A
            or symbol == arcade.key.D
        ):
            self.freesoul.change_x = 0


    def savegame(self):
        with open('savegame.json') as f:
            savedata = json.load(f)
        savedata["checkpoint"] = self.checkpoint
        savedata["time"] = self.timer
        with open('savegame.json', 'w') as f:
            json.dump(savedata, f)


if __name__ == "__main__":
    app = FreeSoulGame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    arcade.run()