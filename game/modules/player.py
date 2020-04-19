import pyglet
from pyglet.window import key

from modules.game_object import GameObject
from modules import util
from modules import bullet

class Player(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        """
        Initializes the player object
        :param game_state: game state
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_player"]]
        # TODO make this a sprite later
        super(Player, self).__init__(img=images[0], *args, **kwargs)

        self.game_state = game_state                # game state object
        self.game_assets = game_assets              # game assets object
        self.type = "player"                        # type of game object

        self.key_handler = key.KeyStateHandler()    # Key press handler
        self.collider_type = "circle"               # Type of collider attached to this object
        self.collision_radius = self.width/2        # collision radius
        self.previous_position = None

        self.height_max = 50

        self.move_step = 10         # Distance by which to move in each key press
        self.life = 100             # Life of the player
        self.bullet_speed = 100     # speed with which a bullet is released

    def inflict_damage(self, amount):
        """
        Inflicts damage to the object. If the life of the object reaches 0, the object dies.
        :param amount: amount of damage to inflict
        """
        self.life -= amount
        if self.life <= 0:
            self.dead = True
        else:
            self.dead = False

    def fire(self):
        """
        Creates a new bullet object and adds it to the list of child objects
        """
        bullet_x = self.x
        bullet_y = self.y + self.height_max / 2
        new_bullet = bullet.Bullet(self.game_state, self.game_assets,
                                   x=bullet_x, y=bullet_y, batch=self.batch,
                                   group=self.group)    # mentioning group is important
        new_bullet.velocity_x = 0
        new_bullet.velocity_y = self.bullet_speed
        self.child_objects.append(new_bullet)

    def on_key_press(self, symbol, modifiers):
        """
        Handle extra key presses (possibly lower frequency presses).
        This function is automatically called by pyglet
        :param symbol: key that has been pressed
        :param modifiers: modifier keys like shift, ctrl and alt
        """
        if symbol == key.SPACE:
            # fire bullet if space is pressed
            self.fire()

    def update_object(self, dt):
        self.previous_position = self.position
        if self.key_handler[key.LEFT]:
            self.x -= self.move_step

        if self.key_handler[key.RIGHT]:
            self.x += self.move_step

        if self.key_handler[key.UP]:
            self.y += self.move_step

        if self.key_handler[key.DOWN]:
            self.y -= self.move_step

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
            # intersection = util.circles_intersection(self.x, self.y,
            #                                          self.collision_radius,
            #                                          other_object.x, other_object.y,
            #                                          other_object.collision_radius)

            # if self.x < other_object.x and self.y < other_object.y:
            #     self.x = intersection[0] - self.collision_radius
            #     self.y = intersection[1] - self.collision_radius
            # elif self.x > other_object.x and self.y < other_object.y:
            #     self.x = intersection[0] + self.collision_radius
            #     self.y = intersection[1] - self.collision_radius
            # elif self.x > other_object.x and self.y > other_object.y:
            #     self.x = intersection[0] + self.collision_radius
            #     self.y = intersection[1] + self.collision_radius
            # elif self.x < other_object.x and self.y < other_object.y:
            #     self.x = intersection[0] - self.collision_radius
            #     self.y = intersection[1] + self.collision_radius
            self.position = self.previous_position
            print("colliding with circle")
        elif other_object.type == "polygon":
            self.dead = False
            self.position = self.previous_position
            print("colliding with polygon")
        elif other_object.type == "bullet":
            self.dead = False   # nothing happens if a bullet hits the object
        elif other_object.type == "virus":
            self.inflict_damage(self.game_state.damage_player_by_virus)
            self.position = self.previous_position      # also bounce back
        elif other_object.type == "virus_particle":
            self.inflict_damage(self.game_state.damage_player_by_virus_particle)