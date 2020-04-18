import random

import pyglet
from pyglet.window import key

from modules.game_object import GameObject
from modules import util


class Virus(GameObject):

    def __init__(self, game_state, game_assets, *args, **kwargs):
        """
        Initializes the player object
        :param game_state: game state
        :param game_assets:
        :param args:
        :param kwargs:
        """
        images = [game_assets.image_assets["img_virus"]]
        # TODO make this a sprite later
        super(Virus, self).__init__(img=images[0], *args, **kwargs)

        self.game_state = game_state                # game state object
        self.type = "virus"                         # type of game object

        self.key_handler = key.KeyStateHandler()    # Key press handler
        self.collider_type = "circle"               # Type of collider attached to this object
        self.collision_radius = self.width/2        # collision radius
        self.previous_position = None

        self.move_step = 0.5     # Distance by which to move in each key press

    def update_object(self, dt):
        self.previous_position = self.position
        self.x += random.randrange(-1, 2, 2) * self.move_step
        self.y += random.randrange(-1, 2, 2) * self.move_step
        self.rotation += random.randrange(-1, 2, 2) * self.move_step

    def handle_collision_with(self, other_object):
        if other_object.type == "circle":
            self.dead = False
            self.position = self.previous_position
        if other_object.type == "virus":
            self.dead = False
            pass
        if other_object.type == "polygon":
            self.dead = False
            self.position = self.previous_position
