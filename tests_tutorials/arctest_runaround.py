# Basic arcade program
# Displays a white window with a blue circle in the middle

# Imports
import arcade
import random
import json

from arcade.key import LEFT

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "FreeSoul v 0.00000000000001"
SCALING = 0.2

# Classes
class FlyingSprite(arcade.Sprite):
    """Base class for all flying sprites: enemies and clouds"""

    def update(self):
        # Move the sprite
        super().update()
        # Remove if off the screen
        if self.right < 0:
            self.remove_from_sprite_lists()

    def remove(self):
        self.remove_from_sprite_lists()

class ArcaneDodger(arcade.Window):
    """Arcane Dodger side scroller game
    freesoul starts on the left, enemies appear on the right
    freesoul can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width, height, title):
        """Initialize the window"""
        # Call the parent class constructor
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.blood_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        self.setup()


    def setup(self):
        """Get the game ready to play"""
        # Set the background color
        arcade.set_background_color(arcade.color.BUD_GREEN)

        # Open saved time record
        f = open("tests_tutorials/records.json")
        records = json.load(f)
        
        # Set state of current playthrough
        self.paused = True
        self.dead = False
        self.timer = 0.0
        self.besttime = records['best_time']

        # Close json file
        f.close()

        # Set up the freesoul
        self.freesoul = arcade.Sprite("images/hero_sword.png", SCALING)
        self.freesoul.center_y = self.height / 2
        self.freesoul.left = 10
        self.all_sprites.append(self.freesoul)

        # Spawn a new enemy every 0.25 seconds
        arcade.schedule(self.add_enemy, 0.18)

        # Spawn a new cloud every second
        #arcade.schedule(self.add_cloud, 1.0)

        # Increment timer in tenths of seconds
        arcade.schedule(self.incrementtimer, 0.1)

    
    def on_draw(self):
        # Draw all game objects
        arcade.start_render()
        arcade.draw_text("You have survived for %4.1f seconds" % self.timer,5,SCREEN_HEIGHT-35,arcade.color.BLACK,30,160,'left',"times new roman")
        arcade.draw_text("Best: %4.1f seconds" % self.besttime,SCREEN_WIDTH-180,SCREEN_HEIGHT-35,arcade.color.BLACK,30,160,'left',"times new roman")
        if self.dead:
            arcade.draw_text("YOU DIED",SCREEN_WIDTH/2-240,SCREEN_HEIGHT/2,arcade.color.RED,80,160,'left',"times new roman")
            arcade.draw_text("Press R to resurrect",SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2-80,arcade.color.RED,30,160,'left',"times new roman")
        if self.paused and not self.dead:
            arcade.draw_text("Paused",SCREEN_WIDTH/2-90,SCREEN_HEIGHT-120,arcade.color.BLACK,60,160,'left',"times new roman")
            arcade.draw_text("Press space to continue",SCREEN_WIDTH/2-170,SCREEN_HEIGHT-160,arcade.color.BLACK,30,160,'left',"times new roman")
        self.all_sprites.draw()
    

    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen
        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """
        if self.paused:
            return
        # Create enemy sprite
        enemy = FlyingSprite("images/spear.png", SCALING)
        # Set its position to a random height and off screen right
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)
        # Set its speed to a random speed heading leftw
        if self.timer > 6:
            enemy.velocity = (random.randint(-int(self.timer), -5), random.randint(-2, 2))
        else:
            enemy.velocity = (random.randint(-6, -5), random.randint(-2, 2))
        # Add it to the enemies list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    """
    def add_cloud(self, delta_time: float):
        #Adds a new cloud
        #Arguments:
        #    delta_time {float} -- How much time since last call
        
        if self.paused:
            return
        # Create new cloud sprite
        cloud = FlyingSprite("images/cloud.png", SCALING)
        # Set position
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height -10)
        # Set speed
        cloud.velocity = (random.randint(-5, -2), 0)
        # Add to enemies' list
        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)
    """

    def add_blood(self):
        # Adds a new blood
        # Create new blood sprite
        blood = FlyingSprite("images/bloodspray01.png", 2.0)
        # Set position
        blood.left = self.freesoul.left
        blood.top = self.freesoul.top
        # Add to blood list
        self.blood_list.append(blood)
        self.all_sprites.append(blood)

    def incrementtimer(self, delta_time: float):
        if not self.paused:
            self.timer = self.timer + delta_time
        if self.timer > self.besttime:
            self.besttime = self.timer

    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects
            If paused, do nothing
        Arguments:
            delta_time {float} -- Time since the last update
        """
        # If paused, don't update anything
        if self.paused:
            return
        # Did you hit anything? If so, end the game
        if self.freesoul.collides_with_list(self.enemies_list):
            self.dead = True
            self.paused = True
            self.add_blood()
            #arcade.close_window()
        # Update everything
        self.all_sprites.update()
        # Keep the freesoul on screen
        if self.freesoul.top > self.height:
            self.freesoul.top = self.height
        if self.freesoul.right > self.width:
            self.freesoul.right = self.width
        if self.freesoul.bottom < 0:
            self.freesoul.bottom = 0
        if self.freesoul.left < 0:
            self.freesoul.left = 0    


    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Q: Quit the game
        P: Pause/Unpause the game
        I/J/K/L: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            f = open('tests_tutorials/records.json', "r")
            savegame = json.load(f)   #savegame is now a Python dictionary
            f.close()
            savegame['best_time'] = self.besttime
            with open('tests_tutorials/records.json', "w") as f:
                json.dump(savegame, f)
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.SPACE:
            if not self.dead:
                self.paused = not self.paused

        if symbol == arcade.key.R:
            if self.dead:
                self.dead = False
                for x in self.enemies_list:
                    x.right = -5   
                for x in self.blood_list:
                    x.remove()
                self.freesoul.center_y = self.height / 2
                self.freesoul.left = 10
                self.timer = 0.0

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.freesoul.change_y = 7

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.freesoul.change_y = -7

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.freesoul.change_x = -7

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.freesoul.change_x = 7


    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released
        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if (
            symbol == arcade.key.W
            or symbol == arcade.key.S
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.freesoul.change_y = 0
        if (
            symbol == arcade.key.A
            or symbol == arcade.key.D
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.freesoul.change_x = 0



# Main code entry point
if __name__ == "__main__":
    app = ArcaneDodger(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    arcade.run()
