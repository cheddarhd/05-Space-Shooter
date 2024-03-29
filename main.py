import sys, logging, os, random, math, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Space Shooter"
STARTING_LOCATION = (250,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
NUM_ENEMIES = 6
HIT_SCORE = 5
KILL_SCORE = 25


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/Starfighter.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("assets/laserblue2.png", 0.3)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage
    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

class Enemy(arcade.Sprite):
    def __init__(self, position):
        super().__init__("assets/shipYellow_manned.png", 0.3)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position


class Window(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)

        self.background = arcade.load_texture("assets/spacebackground.png")
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0

    def setup(self):

        for i in range(NUM_ENEMIES):
            x = 60 * (i+1) + 30
            y = 700
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy) 


    def update(self, delta_time):
        
        self.bullet_list.update()
        self.player.update()
        self.enemy_list.update()
        for e in self.enemy_list:
            damage = arcade.check_for_collision_with_list(e, self.bullet_list)
            for d in damage: 
                e.hp = e.hp - BULLET_DAMAGE
                self.score = self.score + HIT_SCORE
                if e.hp == 0: 
                    e.kill()
                    self.score = self.score + KILL_SCORE

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, 16)


    def on_mouse_motion(self, x, y, dx, dy):
       
        self.player.center_x = x   

    def on_mouse_press(self, x, y, button, modifiers):
        
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,5),BULLET_DAMAGE)
            self.bullet_list.append(bullet)

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            print("Left")
        elif key == arcade.key.RIGHT:
            print("Right")
        elif key == arcade.key.UP:
            print("Up")
        elif key == arcade.key.DOWN:
            print("Down")
        pass

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        pass


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()