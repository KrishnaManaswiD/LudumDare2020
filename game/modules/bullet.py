import pyglet
from pyglet.window import key

from game_object import GameObject
from game_assets import GameAssets

class Bullet(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        """
        Initializes the player object
        :param game_state: game state
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_bullet"]]
        super(Bullet, self).__init__(img=images[0], *args, **kwargs)

        self.game_state = game_state        # game state object
        self.type = "bullet"                # type of game object

        self.key_handler = key.KeyStateHandler()  # Key press handler
        self.collider_type = "circle"  # Type of collider attached to this object
        self.collision_radius = self.width / 2  # collision radius
        self.previous_position = None

        self.move_step = 0.5  # Distance by which to move in each key press
        self.velocity_x = 0
        self.velocity_y = 0

    def update_object(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        pass

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
        elif other_object.type == "virus":
            self.dead = True        # kill myself, damage to virus is handled by the virus
        elif other_object.type == "polygon":
            print("bullet colliding with polygon")
            self.dead = True        # kill myself
        elif other_object.type == "player":
            self.dead = False       # no friendly fire
        elif other_object.type == "virus_particle":
            self.dead = True        # kill myself