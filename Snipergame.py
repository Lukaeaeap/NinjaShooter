import arcade
import random
import math

SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 650
CENTERSCREEN_X = SCREEN_WIDTH/2
CENTERSCREEN_Y = SCREEN_HEIGHT/2
X = SCREEN_WIDTH/2
Y = SCREEN_HEIGHT/2
SCREEN_TITLE = "Ninja sniper"
WALK_RANGE = 100
WALK_SPEED = 1


def calculate_disctance(x, y, x2, y2):  # calculate the distance between two point using pytachoras
    # Difference in x and y
    x_diff = abs(x - x2)
    y_diff = abs(y - y2)
    # pytachoras
    return math.sqrt(x_diff**2 + y_diff**2)  # ** = to the power of


class Enemy:
    def __init__(self, position_x, position_y, change_x, change_y, radius, color, randx, randy):
        """ Take the parameters out of the Enemy class, and create instance variables with the parameters. """
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color
        self.randx = randx
        self.randy = randy

        self.dude = arcade.Sprite("Snipergame/Snipersprites/Ninja.png", 0.5)

    def draw(self):
        """ Tell to our Enemy class how it should draw it. """
        """ only for hitbox showing """  # arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

        self.dude.draw()

    def update(self, delta_time, scope):
        """ Tell to our Enemy class how it should update it. """
        if self.randx+5 >= self.position_x and self.randx-5 <= self.position_x:
            if self.randy+5 >= self.position_y and self.randy-5 <= self.position_y:
                self.randx = (random.randrange(-WALK_RANGE, WALK_RANGE))+self.position_x
                self.randy = (random.randrange(-WALK_RANGE, WALK_RANGE))+self.position_y

        while self.randx > SCREEN_WIDTH-self.radius or self.randx < 0+self.radius:
            self.randx = (random.randrange(-WALK_RANGE, WALK_RANGE))+self.position_x
        while self.randy > SCREEN_HEIGHT-self.radius or self.randy < 0+self.radius:
            self.randy = (random.randrange(-WALK_RANGE, WALK_RANGE))+self.position_y

        if self.randx > self.position_x:
            self.position_x += self.change_x  # * delta_time
        elif self.randx < self.position_x:
            self.position_x -= self.change_x  # * delta_time
        elif self.randy > self.position_y:
            self.position_y += self.change_y  # * delta_time
        elif self.randy < self.position_y:
            self.position_y -= self.change_y  # * delta_time

        self.dude.center_x = self.position_x+4
        self.dude.center_y = self.position_y+4

        # if self.position_x > scope.sniper.position_x-40 and self.position_x < scope.sniper.position_x+40:
        #    print("GAMEOVER")


class Crosshair():
    def __init__(self, position_x, position_y, change_x, change_y, width, height, color):
        """ Take the parameters out of the Crosshair class, and create instance variables with the parameters. """
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.width = width
        self.height = height
        self.color = color

        self.scope = arcade.Sprite("Snipergame/Snipersprites/Crosshair124bit.PNG", 0.5)
        self.sniper = arcade.Sprite("Snipergame/Snipersprites/Sniperpixel.png", 1)
        self.sniper.center_x = SCREEN_WIDTH/2
        self.sniper.center_y = SCREEN_HEIGHT/2

    def draw(self):
        self.sniper.draw()
        self.scope.draw()
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.width, self.height, self.color)

    def update(self, delta_time, left, right):
        """ Tell to our Crosshair class how it should update it. """
        self.scope.center_x = self.position_x-1.01
        self.scope.center_y = self.position_y-1.01

        if left == True:
            self.sniper.turn_left(4)
        if right == True:
            self.sniper.turn_right(4)


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        # Call the parent class's init function to draw the window (standard OOP stuff)
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.set_mouse_visible(False)

        """ Give the classes inits there parameters. """
        self.enemy_list = []
        self.score = 0
        self.wave = -1
        self.wavelength = 0
        self.waveup = False
        self.LEFT = False
        self.RIGHT = False
        self.MOUSCLICKRIGHT = False
        self.RANDX = 0
        self.RANDY = 0
        self.scope = Crosshair(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, X, Y, 5, 5, arcade.color.RED)

    def setup(self):
        print("Let's play ninja sniper")

    def on_draw(self):
        """ Called whenever we need to draw the window, and draw the classes. """
        arcade.start_render()
        for enemy in self.enemy_list:
            enemy.draw()
        self.scope.draw()
        arcade.draw_text(f"Wave: {self.wave}", 10, 50, arcade.color.BLACK, 20)
        arcade.draw_text(f"Kills: {self.score}", 10, 20, arcade.color.BLACK, 20)

    def on_update(self, delta_time):
        """ Update every class every. """
        for enemy in self.enemy_list:
            enemy.update(delta_time, self.scope)
        self.scope.update(delta_time, self.LEFT, self.RIGHT)

        # First we see how long the enemy list is.
        # We draw the amount of ninja's for the length of wavelength.
        Enemy_list_length = len(self.enemy_list)
        if Enemy_list_length == 0:
            self.wave += 1
            for i in range(self.wavelength):
                self.enemy_list.append(Enemy((random.randrange(0, SCREEN_WIDTH)),
                                             (random.randrange(0, SCREEN_HEIGHT)),
                                             WALK_SPEED, WALK_SPEED, 25,
                                             arcade.color.BLACK, self.RANDX, self.RANDY))
            self.wavelength += 1

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.scope.position_x = x
        self.scope.position_y = y

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.LEFT = True
        elif key == arcade.key.RIGHT:
            self.RIGHT = True

    def on_key_release(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.LEFT = False
        if key == arcade.key.RIGHT:
            self.RIGHT = False

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.scope.color = arcade.color.BLACK
            for enemy in self.enemy_list:  # loop over ememy's
                # print(type(enemy))
                if calculate_disctance(x, y, enemy.position_x, enemy.position_y) <= enemy.radius:
                    # enemy hit
                    self.score += 1
                    self.enemy_list.remove(enemy)

    def on_mouse_release(self, x, y, button, modifiers):
        """ Called when a user releases a mouse button. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.scope.color = arcade.color.RED


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

"""
Made by Luuk Hoekstra (2003)
Made in 2020

Credits:
Kuno Zeldenrust for making a few designs and help with some coding
Cas for helping with fixing bugs

"""